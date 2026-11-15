#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT

import os
import subprocess


def shacl2code_generate(args, python_args, outfile):
    p = subprocess.run(
        [
            "shacl2code",
            "generate",
        ]
        + args
        + ["python"]
        + python_args
        + [
            "--output",
            outfile,
        ],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )

    # Add a py.typed file for type checking
    (outfile / "py.typed").touch()
    return p


def run_stubtest(tmp_path, module_name, allowlist=None):
    """
    Run mypy stubtest against a generated package, with no ignore flags.

    `module_name` must be the name of a generated package directory directly
    under `tmp_path`. `allowlist` is an optional stubtest allowlist file.
    """
    pythonpath = os.environ.get("PYTHONPATH")
    if pythonpath:
        pythonpath = os.pathsep.join([str(tmp_path), pythonpath])
    else:
        pythonpath = str(tmp_path)

    env = os.environ.copy()
    env["PYTHONPATH"] = pythonpath

    # No --ignore-missing-stub: a new public symbol must get a stub.
    # No --ignore-unused-allowlist: a stale allowlist entry must be
    # removed instead of silently hiding whatever it matches next.
    cmd = ["stubtest", module_name]
    if allowlist is not None:
        cmd += ["--allow", allowlist]
    subprocess.run(cmd, encoding="utf-8", check=True, env=env)
