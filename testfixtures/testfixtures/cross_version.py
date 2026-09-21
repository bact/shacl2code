#
# Copyright (c) 2026 Joshua Watt
#
# SPDX-License-Identifier: MIT

"""
Cross-version test harness.

Two pieces:

- `generate_versions()`: generate several model versions with the
  `shacl2code generate ... python` CLI, each as its own importable package
  under one directory.
- `check_script()`: run a usage script through one or more static type
  checkers (mypy, pyright, pyrefly) and assert that the set of reported
  error line numbers exactly matches the lines marked with a trailing
  `# expect-error` comment in the script.

check_script() is deliberately paranoid about trusting checker output:
diagnostics are attributed to a file by resolved path (never assumed to be
about the script just because a line number matches), an error reported in
some OTHER file is never silently dropped, and each checker's exit code is
checked against what it actually parsed so a crash or config error can't be
mistaken for "no errors". Every subprocess also runs with its own isolated
cwd (and, for mypy, an explicit empty --config-file and scratch
--cache-dir), so this repository's own pyproject.toml settings (mypy_path,
etc.) can't leak into what's being checked.
"""

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple, Union

EXPECT_ERROR_RE = re.compile(r"#\s*expect-error\s*$")

DEFAULT_CHECKERS = ("mypy", "pyright", "pyrefly")


class CheckerError(RuntimeError):
    """
    A type checker didn't behave the way check_script() needs to trust its
    output -- a crash, a config error, an unrecognized exit code, or (for
    pyright) analyzing zero files. Distinct from AssertionError (a real
    expect-error mismatch), so a broken checker invocation can't be
    silently read as "no errors".
    """


def generate_versions(
    out_dir: Path,
    specs: Sequence[Tuple[str, Sequence[Union[str, Path]], Sequence[str]]],
) -> Dict[str, Path]:
    """
    Generate several Python model versions into one directory.

    `specs` is a sequence of (package_name, shacl_args, python_args):
      - package_name: import name for the generated package, and the
        subdirectory of `out_dir` it's generated into.
      - shacl_args: extra args for `shacl2code generate` (e.g. --input,
        --context), before the `python` subcommand.
      - python_args: extra args for the `python` subcommand itself (e.g.
        --version, --include-protocols), before --output.

    Returns {package_name: package_dir}.
    """
    out_dir = Path(out_dir)
    versions = {}
    for name, shacl_args, python_args in specs:
        pkg_dir = out_dir / name
        subprocess.run(
            ["shacl2code", "generate"]
            + [str(a) for a in shacl_args]
            + ["python"]
            + [str(a) for a in python_args]
            + ["--output", str(pkg_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        # Add a py.typed file for type checking
        (pkg_dir / "py.typed").touch()
        versions[name] = pkg_dir
    return versions


def expected_error_lines(script_path: Path) -> Set[int]:
    """Line numbers (1-based) of lines ending with a `# expect-error` comment."""
    lines = Path(script_path).read_text().splitlines()
    return {i + 1 for i, line in enumerate(lines) if EXPECT_ERROR_RE.search(line)}


def _build_env(pythonpath: Sequence[Union[str, Path]]) -> Dict[str, str]:
    env = os.environ.copy()
    paths = [str(p) for p in pythonpath]
    existing = env.get("PYTHONPATH")
    if existing:
        paths.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def _same_file(reported: str, script_path: Path, cwd: Path) -> bool:
    """
    True if a checker's reported path is script_path. A relative path is
    resolved against the checker's own subprocess cwd, not this process's
    cwd -- pyrefly in particular reports paths relative to it.
    """
    p = Path(reported)
    if not p.is_absolute():
        p = cwd / p
    try:
        return p.resolve() == script_path
    except OSError:
        return False


def _run_mypy(
    script_path: Path, env: Dict[str, str], cwd: Path
) -> Tuple[Set[int], List[str]]:
    cache_dir = cwd / "mypy_cache"
    p = subprocess.run(
        [
            "mypy",
            "--strict",
            # Isolation: ignore any mypy.ini/pyproject.toml/setup.cfg that
            # would otherwise be found by searching upward from cwd (this
            # repo's own pyproject.toml sets mypy_path = testfixtures,
            # which would silently make `import testfixtures` resolve).
            "--config-file=",
            "--cache-dir",
            str(cache_dir),
            "--output",
            "json",
            str(script_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env=env,
        cwd=cwd,
    )
    lines: Set[int] = set()
    other: List[str] = []
    for out_line in p.stdout.splitlines():
        out_line = out_line.strip()
        if not out_line:
            continue
        try:
            obj = json.loads(out_line)
        except json.JSONDecodeError as e:
            raise CheckerError(
                f"mypy produced a non-JSON line (exit {p.returncode}): "
                f"{out_line!r}\nstderr:\n{p.stderr}"
            ) from e
        if obj.get("severity") != "error":
            continue
        if _same_file(obj["file"], script_path, cwd):
            lines.add(obj["line"])
        else:
            other.append(f"{obj['file']}:{obj['line']}: {obj['message']}")

    total = len(lines) + len(other)
    if p.returncode == 0:
        if total:
            raise CheckerError(
                f"mypy exited 0 (no errors) but parsed {total} error "
                f"diagnostic(s) -- harness bug. stdout:\n{p.stdout}"
            )
    elif p.returncode == 1:
        if not total:
            raise CheckerError(
                "mypy exited 1 (errors found) but none were parsed from "
                f"its JSON output -- harness bug.\nstdout:\n{p.stdout}\n"
                f"stderr:\n{p.stderr}"
            )
    else:
        raise CheckerError(
            f"mypy exited {p.returncode} (crash/config error).\n"
            f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        )
    return lines, other


def _run_pyright(
    script_path: Path, env: Dict[str, str], cwd: Path
) -> Tuple[Set[int], List[str]]:
    p = subprocess.run(
        ["pyright", "--outputjson", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env=env,
        cwd=cwd,
    )
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError as e:
        raise CheckerError(
            f"pyright produced non-JSON output (exit {p.returncode}).\n"
            f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        ) from e
    if p.returncode not in (0, 1):
        raise CheckerError(
            f"pyright exited {p.returncode} (crash/config error).\n"
            f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        )
    files_analyzed = data.get("summary", {}).get("filesAnalyzed", 0)
    if files_analyzed < 1:
        raise CheckerError(f"pyright analyzed 0 files -- harness bug: {data}")

    lines: Set[int] = set()
    other: List[str] = []
    for diag in data.get("generalDiagnostics", []):
        if diag.get("severity") != "error":
            continue
        # pyright's JSON line numbers are 0-based
        line = diag["range"]["start"]["line"] + 1
        if _same_file(diag["file"], script_path, cwd):
            lines.add(line)
        else:
            other.append(f"{diag['file']}:{line}: {diag.get('message', '')}")
    return lines, other


def _run_pyrefly(
    script_path: Path, env: Dict[str, str], cwd: Path
) -> Tuple[Set[int], List[str]]:
    p = subprocess.run(
        # "-p default": without a pyrefly.toml, pyrefly falls back to its
        # "basic" preset, which silently disables assignment/call-argument
        # type checking -- exactly the errors this harness needs to catch.
        # Forcing "default" gets normal checking without requiring a config
        # file on disk.
        [
            "pyrefly",
            "check",
            "-p",
            "default",
            "--output-format",
            "json",
            str(script_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env=env,
        cwd=cwd,
    )
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError as e:
        raise CheckerError(
            f"pyrefly produced non-JSON output (exit {p.returncode}).\n"
            f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        ) from e
    if p.returncode not in (0, 1):
        raise CheckerError(
            f"pyrefly exited {p.returncode} (crash/config error).\n"
            f"stdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        )
    errors = data.get("errors")
    if errors is None:
        raise CheckerError(f"pyrefly JSON output missing 'errors' key: {data}")
    if p.returncode == 1 and not errors:
        raise CheckerError(
            "pyrefly exited 1 (errors expected) but parsed zero -- likely "
            f"a crash/config error, not a clean file.\nstdout:\n{p.stdout}\n"
            f"stderr:\n{p.stderr}"
        )

    lines: Set[int] = set()
    other: List[str] = []
    for err in errors:
        if err.get("severity") != "error":
            continue
        if _same_file(err["path"], script_path, cwd):
            lines.add(err["line"])
        else:
            other.append(f"{err['path']}:{err['line']}: {err.get('description', '')}")
    return lines, other


_CHECKER_FUNCS = {
    "mypy": _run_mypy,
    "pyright": _run_pyright,
    "pyrefly": _run_pyrefly,
}


def check_script(
    script_path: Path,
    pythonpath: Union[str, Path, Iterable[Union[str, Path]]],
    checkers: Sequence[str] = DEFAULT_CHECKERS,
) -> None:
    """
    Run each of `checkers` on `script_path` and assert its reported error
    lines exactly match the script's `# expect-error`-marked lines: a
    missing expected error, an unexpected extra error, or an error on the
    wrong line are all failures. An error reported in a file other than
    `script_path` (e.g. inside a generated package being imported) is never
    dropped -- it's an unconditional failure, since generated code isn't
    expected to have type errors of its own.

    `pythonpath` is one or more directories added to PYTHONPATH so the
    script's imports (e.g. of a generated model package) resolve.

    Raises AssertionError on a real mismatch, or CheckerError if a checker
    itself couldn't be trusted (crash, config error, wrong exit code).
    """
    script_path = Path(script_path).resolve()
    expected = expected_error_lines(script_path)

    if isinstance(pythonpath, (str, Path)):
        pythonpath = [pythonpath]
    env = _build_env(list(pythonpath))

    failures: List[str] = []
    with tempfile.TemporaryDirectory(prefix="cross_version_check_") as tmp:
        cwd = Path(tmp)
        for name in checkers:
            actual, other = _CHECKER_FUNCS[name](script_path, env, cwd)
            problems: List[str] = []
            if actual != expected:
                missing = sorted(expected - actual)
                unexpected = sorted(actual - expected)
                problems.append(
                    f"expected error lines {sorted(expected)}, got {sorted(actual)}"
                )
                if missing:
                    problems.append(f"  missing (marked but not reported): {missing}")
                if unexpected:
                    problems.append(
                        f"  unexpected (reported but not marked): {unexpected}"
                    )
            if other:
                problems.append(
                    "  errors reported in OTHER files (never ignored):\n    "
                    + "\n    ".join(other)
                )
            if problems:
                failures.append(f"{name}: " + "\n".join(problems))

    if failures:
        raise AssertionError(
            f"check_script({script_path}) mismatch:\n" + "\n".join(failures)
        )
