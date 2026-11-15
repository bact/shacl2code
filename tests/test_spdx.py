#
# Copyright (c) 2026 Joshua Watt
#
# SPDX-License-Identifier: MIT

import os
import subprocess
import sys
from pathlib import Path

import pytest

from testfixtures.pygen import run_stubtest, shacl2code_generate

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent
TOP_DIR = THIS_DIR.parent

SPDX_DIR = THIS_DIR / "data" / "spdx"

# (module name, fixture directory, URL the context is reported as)
SPDX_VERSIONS = [
    ("spdx301", "3.0.1", "https://spdx.org/rdf/3.0.1/spdx-context.jsonld"),
    ("spdx31rc1", "3.1-dev", "https://spdx.org/rdf/3.1/spdx-context.jsonld"),
]

MODULE_NAMES = [v[0] for v in SPDX_VERSIONS]


@pytest.fixture(scope="module")
def spdx_packages(tmp_path_factory):
    """
    Generate the Python package for each vendored SPDX version, once per
    module. Returns {module name: package directory}; the package's parent
    directory is the import path.
    """
    if not (SPDX_DIR / "3.0.1" / "spdx-model.ttl").exists():
        pytest.skip("tests/data/spdx is not present (excluded from the sdist)")

    out_dir = tmp_path_factory.mktemp("spdx")
    packages = {}
    for name, version_dir, context_url in SPDX_VERSIONS:
        d = SPDX_DIR / version_dir
        shacl2code_generate(
            [
                "--input",
                d / "spdx-model.ttl",
                "--input",
                d / "spdx-json-serialize-annotations.ttl",
                "--context-url",
                d / "spdx-context.jsonld",
                context_url,
            ],
            [],
            out_dir / name,
        )
        packages[name] = out_dir / name
    return packages


@pytest.mark.parametrize("name", MODULE_NAMES)
class TestSpdx:
    """
    Python bindings generated from the vendored SPDX models: the package
    imports, passes flake8, a small script using it passes mypy, and its
    .pyi stubs pass stubtest with no allowlist and no ignore flags.
    """

    def test_import(self, spdx_packages, name):
        subprocess.run(
            [sys.executable, "-c", f"import {name}"],
            cwd=spdx_packages[name].parent,
            check=True,
        )

    def test_flake8(self, spdx_packages, name):
        subprocess.run(
            ["flake8", "--config", TOP_DIR / ".flake8"]
            + list(spdx_packages[name].iterdir()),
            check=True,
        )

    def test_mypy_usage_script(self, spdx_packages, tmp_path, name):
        script = tmp_path / "usage.py"
        script.write_text(
            f"from {name} import Agent\n"
            "\n"
            "\n"
            "def f(a: Agent) -> None:\n"
            "    pass\n"
        )
        subprocess.run(
            [sys.executable, "-m", "mypy", script],
            cwd=tmp_path,
            check=True,
            env={
                **os.environ,
                "MYPYPATH": str(spdx_packages[name].parent),
            },
        )

    def test_stubtest(self, spdx_packages, name):
        run_stubtest(spdx_packages[name].parent, name)
