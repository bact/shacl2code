# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileContributor: Joshua Watt
# SPDX-FileCopyrightText: 2024 Joshua Watt
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT

import json
import re
import subprocess
from pathlib import Path

import jsonschema

import pytest

from testfixtures import jsonvalidation

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent

DATA_DIR = THIS_DIR / "data"

TEST_MODEL = THIS_DIR / "data" / "model" / "test.ttl"

TEST_CONTEXT = THIS_DIR / "data" / "model" / "test-context.json"

SPDX3_CONTEXT_URL = "https://spdx.github.io/spdx-3-model/context.json"


@pytest.mark.parametrize(
    "args",
    [
        ["--input", TEST_MODEL],
        ["--input", TEST_MODEL, "--context-url", TEST_CONTEXT, SPDX3_CONTEXT_URL],
        ["--input", TEST_MODEL, "--jss-signature", "signatures"],
    ],
)
class TestOutput:
    def test_output_syntax(self, args, tmp_path):
        """
        Checks that the output file is valid json syntax by parsing it with Python
        """
        schema_file = tmp_path / "schema.json"

        subprocess.run(
            [
                "shacl2code",
                "generate",
            ]
            + args
            + [
                "jsonschema",
                "--output",
                schema_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

        with schema_file.open("r") as f:
            json.load(f)

    def test_ajv_compile(self, tmp_path, args):
        """
        Validates the generated schema against the JSON Schema meta-schema using ajv
        """
        schema_file = tmp_path / "schema.json"
        subprocess.run(
            [
                "shacl2code",
                "generate",
            ]
            + args
            + [
                "jsonschema",
                "--output",
                schema_file,
            ],
            check=True,
        )
        subprocess.run(
            [
                "node",
                THIS_DIR.parent / "scripts" / "ajv-compile.js",
                str(schema_file),
            ],
            check=True,
        )

    def test_trailing_whitespace(self, args):
        """
        Tests that the generated file does not have trailing whitespace
        """
        p = subprocess.run(
            [
                "shacl2code",
                "generate",
            ]
            + args
            + [
                "jsonschema",
                "--output",
                "-",
            ],
            check=True,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

        for num, line in enumerate(p.stdout.splitlines()):
            assert (
                re.search(r"\s+$", line) is None
            ), f"Line {num + 1} has trailing whitespace"

    def test_tabs(self, args):
        """
        Tests that the output file doesn't contain tabs
        """
        p = subprocess.run(
            [
                "shacl2code",
                "generate",
            ]
            + args
            + [
                "jsonschema",
                "--output",
                "-",
            ],
            check=True,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

        for num, line in enumerate(p.stdout.splitlines()):
            assert "\t" not in line, f"Line {num + 1} has tabs"


@jsonvalidation.validation_tests()
def test_schema_validation(test_jsonschema, test_context_url, passes, data):
    jsonvalidation.replace_context(data, test_context_url)

    if passes:
        jsonschema.validate(data, schema=test_jsonschema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, schema=test_jsonschema)


@jsonvalidation.type_tests()
def test_schema_type_validation(test_jsonschema, test_context_url, passes, data):
    jsonvalidation.replace_context(data, test_context_url)

    if passes:
        jsonschema.validate(data, schema=test_jsonschema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, schema=test_jsonschema)


def test_schema_references(test_jsonschema):
    DEF_PREFIX = "#/$defs/"

    def check_refs(d, path):
        if isinstance(d, dict):
            if "$ref" in d:
                assert d["$ref"].startswith(
                    DEF_PREFIX
                ), f"{''.join(path)} must start with '{DEF_PREFIX}'"
                name = d["$ref"][len(DEF_PREFIX) :]
                assert (
                    name in test_jsonschema["$defs"]
                ), f"{''.join(path)}: {name} is not in $defs"

            for k, v in d.items():
                check_refs(v, path + [f".{k}"])

        if isinstance(d, list):
            for idx, v in enumerate(d):
                check_refs(v, path + [f"[{idx}]"])

    check_refs(test_jsonschema, [])


@pytest.mark.parametrize(
    "passes,extra",
    [
        pytest.param(
            True,
            {"ex1": "http://example.com/", "ex2": "http://bar.com/"},
            id="New prefixes",
        ),
        pytest.param(
            False,
            {"foo": "http://example.com/other"},
            id="Redefine enum value name",
        ),
        pytest.param(
            True,
            {"@vocab": "http://example.com/vocab/"},
            id="Vocabulary for undefined terms",
        ),
        pytest.param(
            False,
            {"test-class": "http://example.com/other"},
            id="Redefine class term",
        ),
        pytest.param(
            False,
            {"test-class/string-scalar-prop": "http://example.com/other"},
            id="Redefine property term",
        ),
        pytest.param(
            False,
            {"test": "http://example.com/other/"},
            id="Redefine prefix",
        ),
        pytest.param(
            False,
            {"ex1": "http://example.com/", "test-class": "http://example.com/x"},
            id="New prefix and redefined term",
        ),
        pytest.param(False, {"@base": "http://example.com/"}, id="Set base"),
        pytest.param(
            False, {"@import": "http://example.com/context.json"}, id="Import"
        ),
        pytest.param(False, {"@language": "en"}, id="Set language"),
        pytest.param(False, {"@direction": "rtl"}, id="Set direction"),
    ],
)
@pytest.mark.parametrize("first", [True, False], ids=["after", "before"])
def test_schema_context_redefinition(
    test_jsonschema, test_context_url, passes, extra, first
):
    """
    Checks that an additional context object cannot change how the terms of
    the model context expand
    """
    if first:
        ctx = [test_context_url, extra]
    else:
        ctx = [extra, test_context_url]

    data = {"@context": ctx, "@graph": []}

    if passes:
        jsonschema.validate(data, schema=test_jsonschema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, schema=test_jsonschema)


@pytest.mark.parametrize(
    "passes,extra",
    [
        pytest.param(True, {"ex1": "http://example.com/"}, id="New prefix"),
        pytest.param(False, {"my-type": "http://example.com/"}, id="Type alias"),
        pytest.param(False, {"my-id": "http://example.com/"}, id="ID alias"),
    ],
)
def test_schema_context_keyword_alias(tmp_path, passes, extra):
    """
    Checks that a term the model context aliases to a keyword cannot be
    redefined by an additional context object
    """
    context_url = "http://example.org/alias-context.json"
    with TEST_CONTEXT.open("r") as f:
        context = json.load(f)
    context["@context"]["my-type"] = "@type"
    context["@context"]["my-id"] = "@id"
    context_file = tmp_path / "context.json"
    with context_file.open("w") as f:
        json.dump(context, f)

    p = subprocess.run(
        [
            "shacl2code",
            "generate",
            "--input",
            TEST_MODEL,
            "--context-url",
            context_file,
            context_url,
            "jsonschema",
            "--output",
            "-",
        ],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    schema = json.loads(p.stdout)

    data = {"@context": [context_url, extra], "@graph": []}

    if passes:
        jsonschema.validate(data, schema=schema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, schema=schema)
