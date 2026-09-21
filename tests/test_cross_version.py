#
# Copyright (c) 2026 Joshua Watt
#
# SPDX-License-Identifier: MIT

"""
Cross-version Protocol test harness and its tests.

This module is test data and harness for the "one function can accept
objects from different model versions" claim, ahead of the generator
actually supporting it -- there is no `--include-protocols` option yet.
Kinds of tests here:

1. Harness self-tests: hand-written tiny scripts and packages that confirm
   `cross_version.check_script()` actually enforces what it claims -- exact
   `# expect-error` line matching, errors attributed to the right FILE (not
   just a coincidentally-matching line number), a checker crash or config
   error never silently read as "no errors", isolation from this
   repository's own pyproject.toml settings, and that a script referencing
   `pkg.protocols.X` needs `import pkg.protocols` specifically -- just
   `import pkg` isn't enough, since `protocols` is a submodule (confirmed
   with a hand-written stand-in `protocols.py` dropped into a generated toy
   package). These pass on main today.
2. SPDX model-level tests: the vendored `tests/data/spdx/3.0.1` and
   `tests/data/spdx/3.1-dev` fixtures generate, import, and type-check
   today, without any Protocol support -- the baseline future Protocol
   support will be measured against. Skipped (not failed) when the
   fixtures are absent, e.g. from an sdist, which deliberately excludes
   them.
3. A scaffolding sanity check: the exact script-building machinery used by
   the (currently xfail) acceptance tests below, run today against a single
   plain model with concrete classes instead of Protocols, asserting zero
   errors -- so once Protocol support lands, any error the real test
   reports is a genuine Protocol problem, not noise from the scaffolding
   itself.
4. Protocol acceptance/rejection tests, marked `xfail(strict=True,
   raises=ProtocolsUnavailable)`: these describe what cross-version
   acceptance and rejection should look like once `--include-protocols`
   exists. On main it isn't a recognized option, so generation itself fails
   with CalledProcessError; `_assert_missing_include_protocols()` checks
   that failure's stderr precisely and only then raises
   ProtocolsUnavailable -- a dedicated exception type, distinct from
   CalledProcessError, so an unrelated CalledProcessError raised anywhere
   else in the test body (e.g. from `_class_names()`/`_class_ancestry()`,
   which run outside that guarded try/except) can't be mistaken for the
   expected failure and silently satisfy `strict=True`; it surfaces as a
   real FAILURE instead.

Every generated script that references a Protocol does `import
<pkg>.protocols` explicitly, not just `import <pkg>` -- `protocols` is a
submodule, and without importing it directly, mypy/pyright treat
`<pkg>.protocols.X` as an unresolved name/attribute rather than the
intended type (see `_build_acceptance_script()` and every hand-written
script below).

Toy model fixtures (test.ttl -> test-v2.ttl -> test-v3.ttl -> test-v4.ttl):
built as purely additive, backward-compatible extensions (new optional
properties, new classes, new enum values, `sh:` deprecation markers) that
keep every existing class's IRI stable across versions. test-v2.ttl adds
test-another-class, used below for the one toy fixture case where an
ordinary structural Protocol check isn't enough on its own (see
test_toy_discriminator_rejects_structurally_compatible_class). test-v3.ttl
and test-v4.ttl chain in test-derived-class-v3 and test-derived-class-v4, a
class added two versions apart from test.ttl, used by
test_toy_multi_version_subclass_accepted to check that a discriminator
keyed by compact name still works across more than one version hop.

None of the additive fixtures can express a changed property type, a
removed property, a scalar/list cardinality flip, or rejecting a versioned
class IRI (IRIs never change). The IRI-keying rejection case is exercised
with the SPDX fixtures instead (their class IRIs do embed the spec
version). The other three are exercised with
tests/data/model/test-breaking-base.ttl and test-breaking.ttl: three small
classes (one per breaking change) in test-breaking-base.ttl, and the SAME
three class names in test-breaking.ttl, each with exactly ONE breaking
change relative to its test-breaking-base.ttl counterpart (test.ttl and
test-context.json aren't touched by either -- their extra context terms
live in test-context-versions.json). One test and one script per class
pair, so a failure is attributable to exactly one change.
"""

import json
import os
import re
import stat
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Dict, List, NoReturn, Sequence, Set

import pytest

from testfixtures import cross_version

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent
TOP_DIR = THIS_DIR.parent

DATA_DIR = THIS_DIR / "data"

TEST_MODEL = DATA_DIR / "model" / "test.ttl"
TEST_V2_MODEL = DATA_DIR / "model" / "test-v2.ttl"
TEST_V4_MODEL = DATA_DIR / "model" / "test-v4.ttl"
TEST_BREAKING_BASE_MODEL = DATA_DIR / "model" / "test-breaking-base.ttl"
TEST_BREAKING_MODEL = DATA_DIR / "model" / "test-breaking.ttl"
# A copy of test-context.json plus entries for the v2/v3/v4/breaking classes
# and properties below. Kept separate (not folded into test-context.json)
# because that file is shared by every other language's tests and must stay
# byte-identical to main.
TEST_CONTEXT = DATA_DIR / "model" / "test-context-versions.json"
# Not fetched -- --context-url only needs a location to load (TEST_CONTEXT)
# and a label to report in the generated code.
TEST_CONTEXT_URL_LABEL = "https://example.org/shacl2code-test/context.json"

SPDX_DIR = DATA_DIR / "spdx"


def _spdx_args(version_dir: str):
    d = SPDX_DIR / version_dir
    return [
        "--input",
        d / "spdx-model.ttl",
        "--input",
        d / "spdx-json-serialize-annotations.ttl",
        "--context",
        f"file://{(d / 'spdx-context.jsonld').resolve()}",
    ]


SPDX_301_ARGS = _spdx_args("3.0.1")
SPDX_31DEV_ARGS = _spdx_args("3.1-dev")


def _spdx_fixtures_present() -> bool:
    return (SPDX_DIR / "3.0.1" / "spdx-model.ttl").exists()


def _skip_if_spdx_fixtures_missing() -> None:
    """
    tests/data/spdx/*/*.ttl and *.jsonld are excluded from the sdist (see
    pyproject.toml) -- skip rather than fail when they're not there.
    """
    if not _spdx_fixtures_present():
        pytest.skip("SPDX fixtures not present (excluded from the sdist)")


TOY_V1_ARGS = [
    "--input",
    TEST_MODEL,
    "--context-url",
    TEST_CONTEXT,
    TEST_CONTEXT_URL_LABEL,
]
TOY_V2_ARGS = [
    "--input",
    TEST_V2_MODEL,
    "--context-url",
    TEST_CONTEXT,
    TEST_CONTEXT_URL_LABEL,
]
TOY_V4_ARGS = [
    "--input",
    TEST_V4_MODEL,
    "--context-url",
    TEST_CONTEXT,
    TEST_CONTEXT_URL_LABEL,
]
TOY_BREAKING_BASE_ARGS = [
    "--input",
    TEST_BREAKING_BASE_MODEL,
    "--context-url",
    TEST_CONTEXT,
    TEST_CONTEXT_URL_LABEL,
]
TOY_BREAKING_ARGS = [
    "--input",
    TEST_BREAKING_MODEL,
    "--context-url",
    TEST_CONTEXT,
    TEST_CONTEXT_URL_LABEL,
]

CHECKERS = ("mypy", "pyright", "pyrefly")


# ---------------------------------------------------------------------------
# 1. Harness self-tests
# ---------------------------------------------------------------------------

GOOD_SCRIPT = textwrap.dedent("""\
    def add(a: int, b: int) -> int:
        return a + b


    def use() -> None:
        add(1, "two")  # expect-error
        ok = add(1, 2)
        print(ok)
    """)

# A tiny hand-written package (no generation needed): regression guard for
# pyrefly's "basic" preset (used automatically when no pyrefly.toml is
# found), which silently disables assignment/call/attribute checks -- it
# reports 0 errors for `mypkg.Persn()` below. check_script() forces
# "-p default" specifically to catch this; mypy --strict and pyright catch
# it either way.
ATTR_TYPO_PACKAGE = textwrap.dedent("""\
    class Person:
        def __init__(self) -> None:
            self.name: str = ""
    """)

ATTR_TYPO_SCRIPT = textwrap.dedent("""\
    import mypkg


    def use() -> None:
        p = mypkg.Persn()  # expect-error
        print(p)
    """)


@pytest.fixture(scope="module")
def attr_typo_pkg(tmp_path_factory):
    pkg_dir = tmp_path_factory.mktemp("attr_typo_pkg")
    (pkg_dir / "mypkg").mkdir()
    (pkg_dir / "mypkg" / "__init__.py").write_text(ATTR_TYPO_PACKAGE)
    (pkg_dir / "mypkg" / "py.typed").touch()
    return pkg_dir


@pytest.mark.parametrize("checker", CHECKERS)
class TestCheckScriptSelfTest:
    """
    Confirms check_script()'s exact-match comparison actually enforces what
    it claims -- a missing, extra, or misplaced marker must fail -- before
    it's trusted to validate anything generated below.
    """

    def test_correct_markers_pass(self, tmp_path, checker):
        script = tmp_path / "script.py"
        script.write_text(GOOD_SCRIPT)
        cross_version.check_script(script, [], checkers=(checker,))

    def test_module_attribute_typo_detected(self, tmp_path, checker, attr_typo_pkg):
        script = tmp_path / "script.py"
        script.write_text(ATTR_TYPO_SCRIPT)
        cross_version.check_script(script, [attr_typo_pkg], checkers=(checker,))

    def test_missing_marker_fails(self, tmp_path, checker):
        """Removing the marker from a real error must fail (unexpected error)."""
        script = tmp_path / "script.py"
        script.write_text(GOOD_SCRIPT.replace("  # expect-error", ""))
        with pytest.raises(AssertionError):
            cross_version.check_script(script, [], checkers=(checker,))

    def test_marker_on_clean_line_fails(self, tmp_path, checker):
        """Adding a marker to a line with no error must fail (missing error)."""
        script = tmp_path / "script.py"
        script.write_text(
            GOOD_SCRIPT.replace("ok = add(1, 2)", "ok = add(1, 2)  # expect-error")
        )
        with pytest.raises(AssertionError):
            cross_version.check_script(script, [], checkers=(checker,))

    def test_marker_on_wrong_line_fails(self, tmp_path, checker):
        """Moving the marker off the real error line must fail either way."""
        script = tmp_path / "script.py"
        text = GOOD_SCRIPT.replace("  # expect-error", "")
        text = text.replace("ok = add(1, 2)", "ok = add(1, 2)  # expect-error")
        script.write_text(text)
        with pytest.raises(AssertionError):
            cross_version.check_script(script, [], checkers=(checker,))


# None of mypy/pyright/pyrefly re-verify the internals of a module reached
# only via `import` (confirmed empirically: a package with a real bug in
# its own body, imported by an otherwise-clean script, reports 0 errors
# from all three checkers -- they only deep-check files given directly on
# the command line). So a realistic "other file" diagnostic can't be
# produced through an ordinary PYTHONPATH import for this self-test; the
# aggregation logic is instead tested directly, by making a fake checker
# function return one, exactly as `_run_mypy`/`_run_pyright`/`_run_pyrefly`
# would if a real checker (or check_script() itself, if ever extended to
# check more than one file) ever did.
def test_other_file_errors_are_never_silently_dropped(tmp_path, monkeypatch):
    """
    An error attributed to a file other than the script must always fail
    check_script() -- even when the script's own expect-error markers
    already match exactly, and even though this can't currently happen via
    an ordinary import (see above). Never silently dropped, regardless.
    """

    def fake_checker(script_path, env, cwd):
        return {1}, ["some/other/file.py:3: a real bug in an imported package"]

    monkeypatch.setitem(cross_version._CHECKER_FUNCS, "mypy", fake_checker)

    script = tmp_path / "script.py"
    script.write_text("x = 1  # expect-error\n")
    with pytest.raises(AssertionError, match="some/other/file.py"):
        cross_version.check_script(script, [], checkers=("mypy",))


# A fake checker executable that always "crashes" -- exits nonzero with no
# parsed diagnostics. Prepending its directory to PATH makes
# subprocess.run(["mypy", ...]) (etc.) invoke it instead of the real tool.
_FAKE_CHECKER_SCRIPT = "#!/bin/sh\necho 'boom: fake checker crashed' 1>&2\nexit 2\n"


@pytest.fixture
def fake_crashing_checkers(tmp_path, monkeypatch):
    bin_dir = tmp_path / "fakebin"
    bin_dir.mkdir()
    for name in CHECKERS:
        p = bin_dir / name
        p.write_text(_FAKE_CHECKER_SCRIPT)
        p.chmod(p.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
    return bin_dir


@pytest.mark.parametrize("checker", CHECKERS)
def test_checker_crash_is_not_read_as_no_errors(
    tmp_path, checker, fake_crashing_checkers
):
    """
    A checker that crashes (nonzero exit, no diagnostics) must raise
    CheckerError, never be silently treated as "0 errors reported".
    """
    script = tmp_path / "script.py"
    script.write_text("x: int = 1\n")
    with pytest.raises(cross_version.CheckerError):
        cross_version.check_script(script, [], checkers=(checker,))


# testfixtures/ (the outer directory, an implicit Python namespace package)
# lives at the repo root. If a checker subprocess runs with the repo root
# as its cwd, `import testfixtures` resolves to that empty namespace
# package purely from cwd -- nothing to do with PYTHONPATH or mypy_path.
# check_script() must not let that happen.
CWD_LEAK_SCRIPT = "import testfixtures  # expect-error\n"


def test_cwd_isolation_prevents_accidental_import(tmp_path):
    script = tmp_path / "script.py"
    script.write_text(CWD_LEAK_SCRIPT)
    cross_version.check_script(script, [], checkers=("mypy",))


@pytest.fixture(scope="module")
def protocols_stand_in_pkg(tmp_path_factory):
    """
    A generated toy package (no --include-protocols needed -- it's not
    implemented yet) with a hand-written `protocols.py` dropped in
    afterwards, standing in for what that flag will eventually generate:
    one Protocol, structurally matching test_class's
    test_class_string_scalar_prop attribute.
    """
    out_dir = tmp_path_factory.mktemp("protocols_stand_in")
    pkg = cross_version.generate_versions(out_dir, [("toyv1", TOY_V1_ARGS, [])])[
        "toyv1"
    ]
    (pkg / "protocols.py").write_text(
        "from typing import Optional, Protocol\n"
        "\n\n"
        "class HasStringScalarProp(Protocol):\n"
        "    test_class_string_scalar_prop: Optional[str]\n"
    )
    return pkg


def test_protocols_submodule_needs_its_own_import(protocols_stand_in_pkg, tmp_path):
    """
    A script that only does `import toyv1` and then refers to
    `toyv1.protocols.X` is wrong: `protocols` is a submodule, not an
    attribute exposed by `import toyv1` alone, so mypy/pyright treat the
    reference itself as an error (a "Name ... is not defined" /
    "not a known attribute" on the annotation, not the intended structural
    mismatch) -- reported on the annotation's line, not on the call the
    test actually cares about.
    """
    script = tmp_path / "missing_submodule_import.py"
    script.write_text(
        "import toyv1\n"
        "\n\n"
        "def f(x: toyv1.protocols.HasStringScalarProp) -> None:\n"
        "    pass\n"
        "\n\n"
        "f(toyv1.test_class())\n"
        "f(toyv1.parent_class())  # expect-error\n"
    )
    with pytest.raises(AssertionError):
        cross_version.check_script(script, pythonpath=[protocols_stand_in_pkg.parent])


def test_protocols_submodule_import_type_checks_clean(protocols_stand_in_pkg, tmp_path):
    """
    With `import toyv1.protocols` too, `toyv1.protocols.HasStringScalarProp`
    is a real type: test_class() (has the attribute) is accepted, and
    parent_class() (test_class's parent, with no own properties -- see
    test_toy_discriminator_rejects_structurally_compatible_class) is
    correctly rejected on structural grounds -- proving both that the
    import fixes name resolution AND that real structural checking is
    happening, not just "no errors because the type didn't resolve".
    """
    script = tmp_path / "stand_in.py"
    script.write_text(
        "import toyv1\n"
        "import toyv1.protocols\n"
        "\n\n"
        "def f(x: toyv1.protocols.HasStringScalarProp) -> None:\n"
        "    pass\n"
        "\n\n"
        "f(toyv1.test_class())\n"
        "f(toyv1.parent_class())  # expect-error\n"
    )
    cross_version.check_script(script, pythonpath=[protocols_stand_in_pkg.parent])


# ---------------------------------------------------------------------------
# ProtocolsUnavailable / _assert_missing_include_protocols() self-tests
# ---------------------------------------------------------------------------


class ProtocolsUnavailable(Exception):
    """
    Raised only by _assert_missing_include_protocols(), and only once it
    has confirmed generation failed specifically because
    --include-protocols isn't a recognized option yet. Deliberately a
    different type from subprocess.CalledProcessError: every xfail test in
    section 4 below uses `raises=ProtocolsUnavailable`, so an unrelated
    CalledProcessError raised anywhere else in the test body (e.g. from
    _class_names()/_class_ancestry(), which run outside the guarded
    try/except around generate_versions()) can't be mistaken for the
    expected failure -- it surfaces as a real FAILURE instead of a
    false-positive XFAIL.
    """


def _fake_called_process_error(stderr: str) -> subprocess.CalledProcessError:
    return subprocess.CalledProcessError(2, ["shacl2code"], output="", stderr=stderr)


_UNRECOGNIZED_INCLUDE_PROTOCOLS_RE = re.compile(
    r"unrecognized arguments:.*--include-protocols"
)


def _assert_missing_include_protocols(exc: subprocess.CalledProcessError) -> NoReturn:
    """
    Confirms `exc` came from argparse rejecting --include-protocols as
    unrecognized -- checked against stderr specifically, not stdout, and
    with a precise pattern, not just a loose substring, so an unrelated
    failure can't be mistaken for this one. Never returns normally: raises
    ProtocolsUnavailable once confirmed, or AssertionError if the failure
    doesn't look like the expected one (a real harness bug).
    """
    stderr = exc.stderr or ""
    assert _UNRECOGNIZED_INCLUDE_PROTOCOLS_RE.search(stderr), (
        "generation failed, but not (apparently) because argparse rejected "
        f"--include-protocols as unrecognized -- possible harness bug. "
        f"stderr:\n{stderr}"
    )
    raise ProtocolsUnavailable(
        "generator doesn't support --include-protocols yet"
    ) from exc


def test_assert_missing_include_protocols_raises_protocols_unavailable():
    exc = _fake_called_process_error(
        "usage: shacl2code [-h] ...\n"
        "shacl2code: error: unrecognized arguments: --include-protocols compact-name\n"
    )
    with pytest.raises(ProtocolsUnavailable):
        _assert_missing_include_protocols(exc)


def test_assert_missing_include_protocols_rejects_unrelated_error():
    """
    The whole point of this check is to distinguish "the flag doesn't
    exist yet" from any other failure. An unrelated CalledProcessError
    must be rejected -- including one that happens to mention
    "include-protocols" for an unrelated reason (e.g. echoing a command
    line), which a loose substring check would wrongly wave through.
    """
    exc = _fake_called_process_error(
        "disk full while writing output for "
        "'shacl2code generate ... --include-protocols compact-name'\n"
    )
    with pytest.raises(AssertionError):
        _assert_missing_include_protocols(exc)


def test_protocols_unavailable_is_not_a_calledprocesserror():
    """See ProtocolsUnavailable's docstring for why this distinction matters."""
    assert not issubclass(ProtocolsUnavailable, subprocess.CalledProcessError)


# ---------------------------------------------------------------------------
# 2. SPDX model-level tests (pass on main today)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def spdx_versions(tmp_path_factory):
    _skip_if_spdx_fixtures_missing()
    out_dir = tmp_path_factory.mktemp("spdx_versions")
    return cross_version.generate_versions(
        out_dir,
        [
            ("spdx301", SPDX_301_ARGS, []),
            ("spdx31dev", SPDX_31DEV_ARGS, []),
        ],
    )


class TestSpdxModelsGenerateNow:
    """
    The vendored SPDX fixtures generate real, working Python bindings on
    main today, without any Protocol support -- the baseline the
    cross-version Protocol claim will be measured against.

    Doesn't run stubtest: that needs an allowlist tuned for the SPDX model,
    which is out of scope here.
    """

    @pytest.mark.parametrize("name", ["spdx301", "spdx31dev"])
    def test_import(self, spdx_versions, name):
        subprocess.run(
            [sys.executable, "-c", f"import {name}"],
            cwd=spdx_versions[name].parent,
            check=True,
        )

    @pytest.mark.parametrize("name", ["spdx301", "spdx31dev"])
    def test_flake8(self, spdx_versions, name):
        pkg_dir = spdx_versions[name]
        subprocess.run(
            ["flake8", "--config", str(TOP_DIR / ".flake8")]
            + [str(f) for f in pkg_dir.iterdir()],
            check=True,
        )

    def test_mypy_usage_script(self, spdx_versions, tmp_path):
        """A trivial script importing one class from each SPDX version type-checks."""
        script = tmp_path / "usage.py"
        script.write_text(
            "from spdx301 import Agent as Agent301\n"
            "from spdx31dev import Agent as Agent31Dev\n"
            "\n"
            "\n"
            "def f(a: Agent301) -> None:\n"
            "    pass\n"
            "\n"
            "\n"
            "def g(a: Agent31Dev) -> None:\n"
            "    pass\n"
        )
        cross_version.check_script(
            script,
            pythonpath=[
                spdx_versions["spdx301"].parent,
                spdx_versions["spdx31dev"].parent,
            ],
            checkers=("mypy",),
        )


# ---------------------------------------------------------------------------
# 3. Shared acceptance/rejection script-building + scaffolding sanity check
# ---------------------------------------------------------------------------


def _class_ancestry(pkg_parent: Path, package_name: str) -> Dict[str, List[str]]:
    """
    {class_name: [names of that class and every subclass of it]}, for every
    model (non-framework) class in `package_name`. Runs in a subprocess so
    it never pollutes this test process's sys.modules/sys.path.
    """
    code = (
        "import json\n"
        f"import {package_name} as pkg\n"
        "by_name = {c.__name__: c for c in set(pkg.SHACLObject.CLASSES.values())}\n"
        "ancestry = {\n"
        "    name: sorted(n for n, c in by_name.items() if issubclass(c, base))\n"
        "    for name, base in by_name.items()\n"
        "}\n"
        "print(json.dumps(ancestry))\n"
    )
    p = subprocess.run(
        [sys.executable, "-c", code],
        cwd=pkg_parent,
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    return json.loads(p.stdout)


def _class_names(pkg_parent: Path, package_name: str) -> Set[str]:
    return set(_class_ancestry(pkg_parent, package_name))


def _build_acceptance_script(
    module_a: str,
    module_b: str,
    common: Sequence[str],
    ancestry: Dict[str, Sequence[str]],
    *,
    use_protocols: bool,
) -> str:
    """
    Build a script with one f_<C>(x: module_a.[protocols.]<C>) -> None per
    class in `common`, called with a `make_<N>()` stub for every class N in
    `ancestry[C]` (module_b's `C` and its subclasses).

    When `use_protocols` is set, module_a's Protocols are referenced as
    `module_a.protocols.<C>` -- which needs `import module_a.protocols`
    specifically, not just `import module_a` (see the module docstring and
    test_protocols_submodule_needs_its_own_import()).

    `make_<N>` bodies `raise NotImplementedError` rather than `...`: mypy
    --strict's empty-body check flags a bare `...` body as an error (code
    `empty-body`) unless the function is an actual stub/overload, which
    would add noise unrelated to what's being tested here. The script is
    only ever type-checked, never executed.
    """
    all_names = sorted({n for names in ancestry.values() for n in names})
    lines = [f"import {module_a}"]
    if use_protocols:
        lines.append(f"import {module_a}.protocols")
    lines.append(f"import {module_b}")
    lines.append("")
    for name in all_names:
        lines.append(f"def make_{name}() -> {module_b}.{name}:")
        lines.append("    raise NotImplementedError")
        lines.append("")
    for name in common:
        target = (
            f"{module_a}.protocols.{name}" if use_protocols else f"{module_a}.{name}"
        )
        lines.append(f"def f_{name}(x: {target}) -> None:")
        lines.append("    pass")
    lines.append("")
    for name in common:
        for sub in ancestry[name]:
            lines.append(f"f_{name}(make_{sub}())")
    return "\n".join(lines) + "\n"


@pytest.fixture(scope="module")
def toy_v1(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("toy_v1")
    return cross_version.generate_versions(out_dir, [("toyv1", TOY_V1_ARGS, [])])[
        "toyv1"
    ]


def test_acceptance_scaffolding_is_clean_on_concrete_classes(toy_v1, tmp_path):
    """
    Sanity check for _build_acceptance_script() itself, run against a
    single plain model (concrete classes, not Protocols, so it needs no
    --include-protocols and passes on main today): the make_<N>() stubs,
    f_<C>() functions, and subclass calls it generates must type-check with
    ZERO errors. This is the same machinery the (currently xfail)
    cross-version acceptance tests use -- if IT were noisy, those tests'
    failures on main wouldn't cleanly isolate to the missing
    --include-protocols flag once it's implemented.
    """
    ancestry = _class_ancestry(toy_v1.parent, "toyv1")
    common = sorted(ancestry)
    script_text = _build_acceptance_script(
        "toyv1", "toyv1", common, ancestry, use_protocols=False
    )
    script = tmp_path / "scaffolding.py"
    script.write_text(script_text)
    cross_version.check_script(script, pythonpath=[toy_v1.parent])


# ---------------------------------------------------------------------------
# 4. Protocol acceptance/rejection tests (data for future Protocol support)
#    -- xfail on main
# ---------------------------------------------------------------------------

_XFAIL_NEEDS_PROTOCOLS = pytest.mark.xfail(
    strict=True,
    raises=ProtocolsUnavailable,
    reason="needs --include-protocols, which the generator doesn't support yet",
)


@_XFAIL_NEEDS_PROTOCOLS
def test_spdx_exhaustive_protocol_acceptance(spdx_versions, tmp_path):
    """
    Exhaustive cross-version acceptance under "compact-name" keying: for
    every class name common to SPDX 3.0.1 and 3.1-dev, a function typed to
    accept 3.0.1's Protocol for that class must also accept a 3.1-dev
    instance of that class or of any 3.1-dev subclass of it. No
    `# expect-error` markers -- everything here is expected to type-check
    cleanly once Protocol support lands.
    """
    p301_names = _class_names(spdx_versions["spdx301"].parent, "spdx301")
    v31_ancestry = _class_ancestry(spdx_versions["spdx31dev"].parent, "spdx31dev")
    common = sorted(p301_names & set(v31_ancestry))
    assert common, "expected overlapping class names between SPDX 3.0.1 and 3.1-dev"

    try:
        versions = cross_version.generate_versions(
            tmp_path / "gen",
            [
                ("spdx301p", SPDX_301_ARGS, ["--include-protocols", "compact-name"]),
                (
                    "spdx31devp",
                    SPDX_31DEV_ARGS,
                    ["--include-protocols", "compact-name"],
                ),
            ],
        )
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    # Unreachable until Protocol support lands.
    script_text = _build_acceptance_script(
        "spdx301p", "spdx31devp", common, v31_ancestry, use_protocols=True
    )
    script = tmp_path / "spdx_exhaustive.py"
    script.write_text(script_text)
    cross_version.check_script(
        script, pythonpath=[versions["spdx301p"].parent, versions["spdx31devp"].parent]
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_spdx_iri_keying_rejects_cross_version(tmp_path):
    """
    "iri" keys each class's Protocol discriminator by its full class IRI,
    which embeds the SPDX spec version (".../3.0.1/..." vs ".../3.1/...").
    A 3.1-dev instance must therefore be rejected by 3.0.1's Protocol for
    the same-named class. Only the SPDX fixtures can exercise this -- see
    the module docstring for why the toy fixtures can't.
    """
    _skip_if_spdx_fixtures_missing()
    try:
        versions = cross_version.generate_versions(
            tmp_path,
            [
                ("spdx301p", SPDX_301_ARGS, ["--include-protocols", "iri"]),
                ("spdx31devp", SPDX_31DEV_ARGS, ["--include-protocols", "iri"]),
            ],
        )
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "iri_keying.py"
    script.write_text(
        "import spdx301p\n"
        "import spdx301p.protocols\n"
        "import spdx31devp\n"
        "\n"
        "\n"
        "def f(x: spdx301p.protocols.Agent) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "def make() -> spdx31devp.Agent:\n"
        "    raise NotImplementedError\n"
        "\n"
        "\n"
        "f(make())  # expect-error\n"
    )
    cross_version.check_script(
        script, pythonpath=[versions["spdx301p"].parent, versions["spdx31devp"].parent]
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_toy_wrong_class_rejected(tmp_path):
    """
    parent_class is test_class's parent and lacks test_class's own
    properties, so a parent_class instance must be rejected by a Protocol
    built from test_class -- an ordinary structural mismatch (this case
    doesn't need the discriminator specifically: parent_class is missing
    real members test_class's Protocol requires).
    """
    try:
        versions = cross_version.generate_versions(
            tmp_path,
            [
                ("toyv1", TOY_V1_ARGS, ["--include-protocols", "compact-name"]),
                ("toyv2", TOY_V2_ARGS, ["--include-protocols", "compact-name"]),
            ],
        )
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "wrong_class.py"
    script.write_text(
        "import toyv1\n"
        "import toyv1.protocols\n"
        "import toyv2\n"
        "\n"
        "\n"
        "def f(x: toyv1.protocols.test_class) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "f(toyv2.parent_class())  # expect-error\n"
    )
    cross_version.check_script(
        script, pythonpath=[versions["toyv1"].parent, versions["toyv2"].parent]
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_toy_discriminator_rejects_structurally_compatible_class(tmp_path):
    """
    parent_class has ZERO own properties in test.ttl (verified at
    generation time by test_acceptance_scaffolding_is_clean_on_concrete_classes
    and by direct introspection during development), so ordinary structural
    typing alone would accept almost anything in its place -- an object
    only needs to have parent_class's (non-existent) members. test-v2.ttl's
    test_another_class has no inheritance relationship to parent_class at
    all (no rdfs:subClassOf). This is exactly the case a discriminator
    exists for: structural typing can't tell them apart, so only the
    version/identity marker can reject test_another_class here.
    """
    try:
        versions = cross_version.generate_versions(
            tmp_path,
            [
                ("toyv1", TOY_V1_ARGS, ["--include-protocols", "compact-name"]),
                ("toyv2", TOY_V2_ARGS, ["--include-protocols", "compact-name"]),
            ],
        )
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "discriminator.py"
    script.write_text(
        "import toyv1\n"
        "import toyv1.protocols\n"
        "import toyv2\n"
        "\n"
        "\n"
        "def f(x: toyv1.protocols.parent_class) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "f(toyv2.test_another_class())  # expect-error\n"
    )
    cross_version.check_script(
        script, pythonpath=[versions["toyv1"].parent, versions["toyv2"].parent]
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_toy_multi_version_subclass_accepted(tmp_path):
    """
    test_derived_class_v4 (added in test-v4.ttl, subclassing
    test_derived_class_v3 from test-v3.ttl, which subclasses
    test_derived_class from test.ttl) must satisfy test.ttl's Protocol for
    test_derived_class even though it's two version increments removed --
    confirms compact-name keying survives more than one version hop, not
    just adjacent versions.
    """
    try:
        versions = cross_version.generate_versions(
            tmp_path,
            [
                ("toyv1", TOY_V1_ARGS, ["--include-protocols", "compact-name"]),
                ("toyv4", TOY_V4_ARGS, ["--include-protocols", "compact-name"]),
            ],
        )
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "multi_version.py"
    script.write_text(
        "import toyv1\n"
        "import toyv1.protocols\n"
        "import toyv4\n"
        "\n"
        "\n"
        "def f(x: toyv1.protocols.test_derived_class) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "def make() -> toyv4.test_derived_class_v4:\n"
        "    raise NotImplementedError\n"
        "\n"
        "\n"
        "f(make())\n"
    )
    cross_version.check_script(
        script, pythonpath=[versions["toyv1"].parent, versions["toyv4"].parent]
    )


def _generate_breaking_versions(tmp_path: Path) -> Dict[str, Path]:
    return cross_version.generate_versions(
        tmp_path,
        [
            (
                "toybreakingbase",
                TOY_BREAKING_BASE_ARGS,
                ["--include-protocols", "compact-name"],
            ),
            (
                "toybreaking",
                TOY_BREAKING_ARGS,
                ["--include-protocols", "compact-name"],
            ),
        ],
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_toy_breaking_type_change_rejected(tmp_path):
    """
    breaking-type-class's `value` changed type string (test-breaking-base
    .ttl) -> integer (test-breaking.ttl). Same class name in both, so a
    compact-name/iri discriminator alone would accept it, but structural
    typing must reject it regardless.
    """
    try:
        versions = _generate_breaking_versions(tmp_path)
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "breaking_type_change.py"
    script.write_text(
        "import toybreakingbase\n"
        "import toybreakingbase.protocols\n"
        "import toybreaking\n"
        "\n"
        "\n"
        "def f(x: toybreakingbase.protocols.breaking_type_class) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "f(toybreaking.breaking_type_class())  # expect-error\n"
    )
    cross_version.check_script(
        script,
        pythonpath=[
            versions["toybreakingbase"].parent,
            versions["toybreaking"].parent,
        ],
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_toy_breaking_removed_property_rejected(tmp_path):
    """
    breaking-removed-class's `value` property exists in
    test-breaking-base.ttl and is removed entirely in test-breaking.ttl. A
    Protocol built from the base class requires it, so structural typing
    must reject a test-breaking.ttl instance outright (the whole object is
    missing a required member), regardless of the discriminator.
    """
    try:
        versions = _generate_breaking_versions(tmp_path)
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "breaking_removed_property.py"
    script.write_text(
        "import toybreakingbase\n"
        "import toybreakingbase.protocols\n"
        "import toybreaking\n"
        "\n"
        "\n"
        "def f(x: toybreakingbase.protocols.breaking_removed_class) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "f(toybreaking.breaking_removed_class())  # expect-error\n"
    )
    cross_version.check_script(
        script,
        pythonpath=[
            versions["toybreakingbase"].parent,
            versions["toybreaking"].parent,
        ],
    )


@_XFAIL_NEEDS_PROTOCOLS
def test_toy_breaking_cardinality_flip_rejected(tmp_path):
    """
    breaking-cardinality-class's `value` is a list in
    test-breaking-base.ttl and flipped to a scalar in test-breaking.ttl. A
    Protocol built from the base class expects a list-shaped member there,
    so structural typing must reject it regardless of the discriminator
    (this is the realistic-to-miss case: `str` is itself `Iterable[str]`,
    so a checker that isn't actually doing structural checking here could
    wrongly accept a scalar str in place of a list).
    """
    try:
        versions = _generate_breaking_versions(tmp_path)
    except subprocess.CalledProcessError as e:
        _assert_missing_include_protocols(e)

    script = tmp_path / "breaking_cardinality_flip.py"
    script.write_text(
        "import toybreakingbase\n"
        "import toybreakingbase.protocols\n"
        "import toybreaking\n"
        "\n"
        "\n"
        "def f(x: toybreakingbase.protocols.breaking_cardinality_class) -> None:\n"
        "    pass\n"
        "\n"
        "\n"
        "f(toybreaking.breaking_cardinality_class())  # expect-error\n"
    )
    cross_version.check_script(
        script,
        pythonpath=[
            versions["toybreakingbase"].parent,
            versions["toybreaking"].parent,
        ],
    )
