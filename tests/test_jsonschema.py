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


@pytest.fixture(scope="module")
def extra_contexts_jsonschema(model_server, test_context_url):
    p = subprocess.run(
        [
            "shacl2code",
            "generate",
            "--input",
            TEST_MODEL,
            "--context",
            test_context_url,
            "--jss-signature",
            "signatures",
            "jsonschema",
            "--allow-extra-contexts",
            "--output",
            "-",
        ],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    yield json.loads(p.stdout)


def test_extra_contexts_off_unchanged(model_server, test_context_url, tmp_path):
    """
    Checks that the schema is unchanged when --allow-extra-contexts is not
    given
    """
    p = subprocess.run(
        [
            "shacl2code",
            "generate",
            "--input",
            TEST_MODEL,
            "--context",
            test_context_url,
            "jsonschema",
            "--output",
            "-",
        ],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    schema = json.loads(p.stdout)
    assert "ExtraContext" not in schema["$defs"]
    assert "ExtensibleTypeTerm" not in schema["$defs"]


CONTEXT_PLACEHOLDER = "@CONTEXT@"

EXTRA_CONTEXT_OBJ = {
    "ex": "http://example.com/",
    "exProp": {"@id": "ex:foo", "@type": "@id"},
}


@pytest.mark.parametrize(
    "passes,context",
    [
        pytest.param(True, [CONTEXT_PLACEHOLDER], id="Array"),
        pytest.param(True, CONTEXT_PLACEHOLDER, id="Single"),
        pytest.param(
            True,
            [CONTEXT_PLACEHOLDER, "http://example.com/context.jsonld"],
            id="Context IRI",
        ),
        pytest.param(
            True,
            [CONTEXT_PLACEHOLDER, EXTRA_CONTEXT_OBJ],
            id="Context object",
        ),
        pytest.param(
            True,
            [
                CONTEXT_PLACEHOLDER,
                "http://example.com/context.jsonld",
                {"@version": 1.1, "@protected": True, **EXTRA_CONTEXT_OBJ},
            ],
            id="Context IRI and object",
        ),
        pytest.param(
            True,
            [
                CONTEXT_PLACEHOLDER,
                {
                    "ex": "http://example.com/",
                    "exProp": {"@id": "ex:foo", "@context": {"exSub": "ex:bar"}},
                },
            ],
            id="Property-scoped context",
        ),
        pytest.param(
            False,
            ["http://example.com/context.jsonld", CONTEXT_PLACEHOLDER],
            id="Model context not first",
        ),
        pytest.param(
            False,
            [EXTRA_CONTEXT_OBJ, CONTEXT_PLACEHOLDER],
            id="Context object before model context",
        ),
        pytest.param(False, [EXTRA_CONTEXT_OBJ], id="No model context"),
        pytest.param(False, "http://example.com/context.jsonld", id="Other IRI"),
        pytest.param(False, [CONTEXT_PLACEHOLDER, None], id="Null context"),
        pytest.param(False, [CONTEXT_PLACEHOLDER, "not-an-iri"], id="Relative IRI"),
        pytest.param(False, [CONTEXT_PLACEHOLDER, 1], id="Number"),
        pytest.param(
            False,
            [CONTEXT_PLACEHOLDER, {"test-class": "http://example.com/other"}],
            id="Redefine model term",
        ),
        pytest.param(
            False,
            [CONTEXT_PLACEHOLDER, {"test-class": {"@id": "http://example.com/x"}}],
            id="Redefine model term with term definition",
        ),
        pytest.param(
            False,
            [CONTEXT_PLACEHOLDER, {"@base": "http://example.com/"}],
            id="Set base",
        ),
        pytest.param(
            False,
            [CONTEXT_PLACEHOLDER, {"@import": "http://example.com/context.json"}],
            id="Import",
        ),
        pytest.param(
            False,
            [
                CONTEXT_PLACEHOLDER,
                {
                    "exProp": {
                        "@id": "http://example.com/foo",
                        "@context": {"test-class": "http://example.com/other"},
                    }
                },
            ],
            id="Property-scoped context redefines model term",
        ),
        pytest.param(
            False,
            [
                CONTEXT_PLACEHOLDER,
                {
                    "exProp": {
                        "@id": "http://example.com/foo",
                        "@context": [
                            "http://example.com/context.jsonld",
                            {"@base": "http://example.com/"},
                        ],
                    }
                },
            ],
            id="Property-scoped context array sets base",
        ),
        pytest.param(
            False,
            [
                CONTEXT_PLACEHOLDER,
                {
                    "exProp": {
                        "@id": "http://example.com/foo",
                        "@context": {
                            "bar": {
                                "@id": "http://example.com/bar",
                                "@context": {"test": "http://example.com/x/"},
                            }
                        },
                    }
                },
            ],
            id="Nested property-scoped context redefines model prefix",
        ),
        pytest.param(
            False,
            [
                CONTEXT_PLACEHOLDER,
                {"exProp": {"@id": "http://example.com/foo", "@context": None}},
            ],
            id="Property-scoped null context",
        ),
    ],
)
def test_extra_contexts(extra_contexts_jsonschema, test_context_url, passes, context):
    """
    Checks the @context accepted with --allow-extra-contexts
    """

    def replace(c):
        if c == CONTEXT_PLACEHOLDER:
            return test_context_url
        if isinstance(c, list):
            return [replace(i) for i in c]
        return c

    data = {"@context": replace(context), "@graph": []}

    if passes:
        jsonschema.validate(data, schema=extra_contexts_jsonschema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, schema=extra_contexts_jsonschema)


@pytest.mark.parametrize(
    "passes_on,passes_off,type_name",
    [
        pytest.param(True, True, "extensible-class", id="Model class"),
        pytest.param(True, True, "http://example.com/extended", id="IRI"),
        pytest.param(True, True, "ex:extended", id="Compact IRI"),
        pytest.param(True, False, "extended", id="Term"),
        pytest.param(False, False, "test-class", id="Other model class"),
        pytest.param(False, False, "abstract-class", id="Abstract model class"),
        pytest.param(False, False, "@id", id="Keyword"),
    ],
)
@pytest.mark.parametrize("nested", [False, True], ids=["root", "nested"])
def test_extra_contexts_extensible_type(
    test_jsonschema,
    extra_contexts_jsonschema,
    test_context_url,
    passes_on,
    passes_off,
    type_name,
    nested,
):
    """
    Checks that with --allow-extra-contexts, an extensible class may have a
    type that is a term (no ":") defined by an additional context
    """
    obj = {
        "@type": type_name,
        "extensible-class/required": "foo",
    }
    if nested:
        obj = {"@type": "link-class", "link-class-extensible": obj}

    data = {
        "@context": [
            test_context_url,
            {"ex": "http://example.com/", "extended": "ex:extended"},
        ],
        **obj,
    }

    for schema, passes in (
        (extra_contexts_jsonschema, passes_on),
        (test_jsonschema, passes_off),
    ):
        if schema is test_jsonschema:
            # Without the option, the context object may not add term
            # definitions, only prefixes
            data["@context"] = [test_context_url, {"ex": "http://example.com/"}]

        if passes:
            jsonschema.validate(data, schema=schema)
        else:
            with pytest.raises(jsonschema.ValidationError):
                jsonschema.validate(data, schema=schema)


# Shared validation tests whose result is expected to differ with
# --allow-extra-contexts
EXTRA_CONTEXTS_CHANGED = {
    # The model context must come first
    "Extended context (alternate order)",
    # A context IRI after the model context is allowed
    "Multiple context with bad URL",
    # Without a colon, a type is a term, which may be an extension class
    "Nested extensible class with non-IRI type",
}


@jsonvalidation.validation_tests()
def test_extra_contexts_validation(
    request, extra_contexts_jsonschema, test_context_url, passes, data
):
    jsonvalidation.replace_context(data, test_context_url)

    if request.node.callspec.id in EXTRA_CONTEXTS_CHANGED:
        passes = not passes

    if passes:
        jsonschema.validate(data, schema=extra_contexts_jsonschema)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, schema=extra_contexts_jsonschema)
