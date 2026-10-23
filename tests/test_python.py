#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT

import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jsonschema

import pyshacl

import pytest

import rdflib

from testfixtures import jsonvalidation, timetests

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent
TOP_DIR = THIS_DIR.parent

DATA_DIR = THIS_DIR / "data"

TEST_MODEL = THIS_DIR / "data" / "model" / "test.ttl"

TEST_CONTEXT = THIS_DIR / "data" / "model" / "test-context.json"

SPDX3_CONTEXT_URL = "https://spdx.github.io/spdx-3-model/context.json"

TEST_TZ = timezone(timedelta(hours=-2), name="TST")

MODEL_VERSION = "1.0.0.alpha"

VALIDATION_ERROR = object()

ENCODE_ERROR = object()


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


@pytest.fixture(scope="module")
def python_model(tmp_path_factory, test_context_url):
    tmp_directory = tmp_path_factory.mktemp("pythontestcontext")
    module_name = "pymodel"
    output_dir = tmp_directory / module_name
    shacl2code_generate(
        [
            "--input",
            TEST_MODEL,
            "--context",
            test_context_url,
            "--jss-signature",
            "signatures",
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir,
    )
    yield tmp_directory, module_name


@pytest.fixture
def python_model_env(python_model):
    module_path, module_name = python_model
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        env.get("PYTHONPATH", "").split(os.pathsep) + [str(module_path)]
    )
    return env, module_name


@pytest.fixture(scope="module")
def model_script(tmp_path_factory, python_model):
    tmp_directory = tmp_path_factory.mktemp("pythonmodelscript")
    module_path, module_name = python_model

    script = tmp_directory / "script.py"
    script.write_text(textwrap.dedent(f"""\
        #! /usr/bin/env python3
        import sys
        sys.path.append("{module_path}")

        import {module_name}

        sys.exit({module_name}.main())
        """))
    script.chmod(0o755)
    yield script


@pytest.fixture(scope="function")
def model(python_model):
    module_path, module_name = python_model

    old_path = sys.path[:]
    sys.path.append(str(module_path))
    try:
        # Reload all model modules
        for m in list(sys.modules):
            if m == module_name or m.startswith(module_name + "."):
                importlib.reload(sys.modules[m])
        yield importlib.import_module(module_name)
    finally:
        sys.path = old_path


MODEL_TESTS = (
    "args,python_args",
    [
        pytest.param(
            ["--input", TEST_MODEL],
            [],
            id="Model",
        ),
        pytest.param(
            ["--input", TEST_MODEL, "--context-url", TEST_CONTEXT, SPDX3_CONTEXT_URL],
            [],
            id="Context URL",
        ),
        pytest.param(
            ["--input", TEST_MODEL],
            ["--include-main=no"],
            id="No main",
        ),
        pytest.param(["--input", TEST_MODEL], ["--version=1.0.0"], id="Version"),
        pytest.param(
            ["--input", TEST_MODEL, "--jss-signature", "signatures"],
            [],
            id="JSS Signature",
        ),
    ],
)


@pytest.mark.parametrize(*MODEL_TESTS)
class TestOutput:
    """
    Test syntax and formatting of the output file
    """

    def test_output_syntax(self, model_script, args, python_args):
        """
        Checks that the output file is valid python syntax by executing it"
        """
        subprocess.run([model_script, "--help"], check=True)

    def test_trailing_whitespace(self, tmp_path, args, python_args):
        """
        Tests that the generated file does not have trailing whitespace
        """
        output_dir = tmp_path / "output"
        shacl2code_generate(args, python_args, output_dir)

        for p in output_dir.iterdir():
            for num, line in enumerate(p.read_text().splitlines()):
                assert (
                    re.search(r"\s+$", line) is None
                ), f"{p}: Line {num + 1} has trailing whitespace"

    def test_tabs(self, tmp_path, args, python_args):
        """
        Tests that the output file doesn't contain tabs
        """
        output_dir = tmp_path / "output"
        shacl2code_generate(args, python_args, output_dir)

        for p in output_dir.iterdir():
            for num, line in enumerate(p.read_text().splitlines()):
                assert "\t" not in line, f"{p}: Line {num + 1} has tabs"


@pytest.mark.parametrize(*MODEL_TESTS)
class TestCheckType:
    """
    Static type checking tests for the generated Python code
    """

    def test_mypy(self, tmp_path, args, python_args):
        """
        Mypy static type checking
        """
        output_dir = tmp_path / "pymodel"
        shacl2code_generate(args, python_args, output_dir)
        subprocess.run(
            ["mypy", output_dir],
            encoding="utf-8",
            check=True,
        )
        # Run again on just the .py files
        subprocess.run(
            ["mypy"] + [f for f in output_dir.iterdir() if f.suffix == ".py"],
            encoding="utf-8",
            check=True,
        )

    def test_stubtest(self, tmp_path, args, python_args):
        """
        Mypy stub checks to ensure pyi stubs are in sync with py code
        """
        output_dir = tmp_path / "pymodel"
        shacl2code_generate(args, python_args, output_dir)

        pythonpath = os.environ.get("PYTHONPATH")
        if pythonpath:
            pythonpath = os.pathsep.join(str(tmp_path), pythonpath)
        else:
            pythonpath = str(tmp_path)

        env = os.environ.copy()
        env["PYTHONPATH"] = pythonpath

        subprocess.run(
            [
                "stubtest",
                "pymodel",
                "--allow",
                DATA_DIR / "stubtest" / "allow.txt",
                "--ignore-unused-allowlist",
                "--ignore-missing-stub",
            ],
            encoding="utf-8",
            check=True,
            env=env,
        )

    def test_pyrefly(self, tmp_path, args, python_args):
        """
        Pyrefly static type checking
        """
        output_dir = tmp_path / "pymodel"
        shacl2code_generate(args, python_args, output_dir)
        subprocess.run(
            ["pyrefly", "check", "--search-path", tmp_path]
            + list(output_dir.iterdir()),
            encoding="utf-8",
            check=True,
        )

    def test_pyright(self, tmp_path, args, python_args):
        """
        Pyright static type checking
        """
        output_dir = tmp_path / "pymodel"
        shacl2code_generate(args, python_args, output_dir)
        subprocess.run(
            ["pyright"] + list(output_dir.iterdir()),
            encoding="utf-8",
            check=True,
        )

    def test_flake8(self, tmp_path, args, python_args):
        """
        Flake8 linting
        """
        output_dir = tmp_path / "pymodel"
        shacl2code_generate(args, python_args, output_dir)
        subprocess.run(
            ["flake8", "--config", TOP_DIR / ".flake8"] + list(output_dir.iterdir()),
            encoding="utf-8",
            check=True,
        )

    def test_bandit(self, tmp_path, args, python_args):
        """
        Bandit security linting
        """
        output_dir = tmp_path / "pymodel"
        shacl2code_generate(args, python_args, output_dir)
        subprocess.run(
            ["bandit", "-r", output_dir],
            encoding="utf-8",
            check=True,
        )


@pytest.fixture
def python_usage_script(python_model_env, tmp_path):
    env, module_name = python_model_env

    script_path = tmp_path / "script.py"
    script_path.write_text(textwrap.dedent(f"""
            #! /usr/bin/env python3
            from typing import ClassVar, Iterable, List, Union
            import {module_name}

            print({module_name}.enumType.foo)

            class OERecipeExtension({module_name}.extensible_abstract_class):
                TYPE: ClassVar[str] = "http://example.org/shacl2code-test/recipe-extension"
                NODE_KIND: ClassVar[{module_name}.NodeKind] = {module_name}.NodeKind.BlankNodeOrIRI
                PROPERTIES: ClassVar[List[{module_name}.ClassProp]] = [
                    {module_name}.ClassProp(
                        "is_native",
                        lambda: {module_name}.BooleanProp(),
                        iri="http://example.org/shacl2code-test/is-native",
                        max_count=1,
                    ),
                ]

            def test1(o: {module_name}.link_class) -> int:
                return len(o.link_class_link_list_prop)

            def test2(o: {module_name}.link_class) -> Iterable[Union[{module_name}.link_class, str]]:
                yield from o.link_class_link_list_prop

            def test3(a: {module_name}.link_class, b: {module_name}.link_class) -> bool:
                return a in b.link_class_link_list_prop

            def test4(lst: Iterable[{module_name}.SHACLObject]) -> List[{module_name}.SHACLObject]:
                return sorted(lst)
            """))

    # Validate the script runs
    subprocess.run([sys.executable, script_path], env=env, check=True)
    yield env, script_path


class TestUsageType:
    def test_mypy(self, python_usage_script):
        env, script_path = python_usage_script
        subprocess.run(
            ["mypy", script_path],
            encoding="utf-8",
            env=env,
            check=True,
        )

    def test_pyright(self, python_usage_script):
        env, script_path = python_usage_script
        subprocess.run(
            ["pyright", script_path],
            encoding="utf-8",
            env=env,
            check=True,
        )

    def test_pyrefly(self, python_usage_script):
        env, script_path = python_usage_script
        subprocess.run(
            ["pyrefly", "check", script_path],
            encoding="utf-8",
            env=env,
            check=True,
        )


def check_file(p, expect, digest):
    sha1 = hashlib.sha1()
    with p.open("rb") as f:
        while True:
            d = f.read(4096)
            if not d:
                break
            sha1.update(d)

    assert sha1.hexdigest() == digest

    with p.open("r") as f:
        data = json.load(f)

    assert data == expect


def test_roundtrip(model, tmp_path, roundtrip):
    doc = model.SHACLObjectSet()
    with roundtrip.open("r") as f:
        d = model.JSONLDDeserializer()
        d.read(f, doc)

    with roundtrip.open("r") as f:
        expect_data = json.load(f)

    outfile = tmp_path / "out.json"
    with outfile.open("wb") as f:
        s = model.JSONLDSerializer()
        digest = s.write(doc, f, indent=4)

    check_file(outfile, expect_data, digest)

    with outfile.open("wb") as f:
        s = model.JSONLDInlineSerializer()
        digest = s.write(doc, f)

    check_file(outfile, expect_data, digest)


def test_script_roundtrip(model_script, tmp_path, roundtrip):
    outpath = tmp_path / "out.json"

    subprocess.run(
        [model_script, roundtrip, "--outfile", outpath],
        check=True,
    )

    with roundtrip.open("r") as f:
        expect_data = json.load(f)

    with outpath.open("r") as f:
        data = json.load(f)

    assert data == expect_data


def test_module_roundtrip(python_model_env, tmp_path, roundtrip):
    env, module_name = python_model_env

    outpath = tmp_path / "out.json"
    subprocess.run(
        [sys.executable, "-m", module_name, roundtrip, "--outfile", outpath],
        check=True,
        env=env,
    )

    with roundtrip.open("r") as f:
        expect_data = json.load(f)

    with outpath.open("r") as f:
        data = json.load(f)

    assert data == expect_data


def test_from_rdf_roundtrip(model, tmp_path, roundtrip):
    with roundtrip.open("r") as f:
        expect_data = json.load(f)

    # Parse data using RDF
    g = rdflib.Graph()
    g.parse(roundtrip)

    # Convert to SHACL objects
    objset = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset)

    # Copy context from expected roundtrip file (RDF doesn't preserve context)
    model.decode_context(model.JSONLDDecoder(expect_data["@context"]), objset)

    # Write out
    outfile = tmp_path / "out.json"
    with outfile.open("wb") as f:
        digest = model.JSONLDInlineSerializer().write(objset, f)

    check_file(outfile, expect_data, digest)


def test_to_rdf_roundtrip(model, tmp_path, roundtrip):
    with roundtrip.open("r") as f:
        expect_data = json.load(f)

    # Read JSON data
    objset = model.SHACLObjectSet()
    with roundtrip.open("r") as f:
        model.JSONLDDeserializer().read(f, objset)

    # Convert to RDF
    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)

    # Convert from RDF to new object set
    objset = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset)

    # Copy context from expected roundtrip file (RDF doesn't preserve context)
    model.decode_context(model.JSONLDDecoder(expect_data["@context"]), objset)

    # Write out
    outfile = tmp_path / "out.json"
    with outfile.open("wb") as f:
        digest = model.JSONLDInlineSerializer().write(objset, f)

    check_file(outfile, expect_data, digest)


def test_jsonschema_validation(roundtrip, test_jsonschema):
    with roundtrip.open("r") as f:
        data = json.load(f)

    jsonschema.validate(data, schema=test_jsonschema)


@jsonvalidation.validation_tests()
def test_json_validation(passes, data, tmp_path, test_context_url, model_script):
    jsonvalidation.replace_context(data, test_context_url)

    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps(data))

    p = subprocess.run([model_script, data_file, "--outfile", os.devnull], check=False)
    if passes:
        assert p.returncode == 0
    else:
        assert p.returncode != 0


@jsonvalidation.link_tests()
def test_links(filename, name, expect_tag, model, tmp_path, test_context_url):
    data_file = tmp_path / "data.json"
    data_file.write_text(
        filename.read_text().replace("@CONTEXT_URL@", test_context_url)
    )

    objset = model.SHACLObjectSet()
    with data_file.open("r") as f:
        deserializer = model.JSONLDDeserializer()
        deserializer.read(f, objset)

    c = objset.find_by_id(name)
    assert isinstance(c, model.link_class)

    for o in objset.foreach_type(model.link_class):
        if o.link_class_tag == expect_tag:
            link = o
            break
    else:
        assert False, f"Unable to find object with tag '{expect_tag}'"

    assert c.link_class_link_prop is link
    assert c.link_class_link_prop_no_class is link
    assert c.link_class_link_list_prop == [link, link]


@pytest.mark.parametrize(
    "filename,expect,match",
    [
        pytest.param(
            "bad-object-type-inline.json",
            VALIDATION_ERROR,
            "Type test-class is not valid where",
            id="Bad object type for property (inline)",
        ),
        pytest.param(
            "bad-object-type-ref-before.json",
            VALIDATION_ERROR,
            "Value must be one of type: link_class, str. Got test_class",
            id="Bad object type for property (linked by ID before)",
        ),
        pytest.param(
            "bad-object-type-ref-after.json",
            VALIDATION_ERROR,
            "Value must be one of type: link_class, str. Got test_class",
            id="Bad object type for property (linked by ID after)",
        ),
    ],
)
def test_deserialize(filename, expect, match, model, test_context_url):
    objset = model.SHACLObjectSet()
    deserializer = model.JSONLDDeserializer()
    with (DATA_DIR / "python" / filename).open("r") as f:
        d = json.loads(f.read().replace("@CONTEXT_URL@", test_context_url))

    if expect is VALIDATION_ERROR:
        expect = model.ValidationError

    if issubclass(expect, Exception):
        with pytest.raises(expect, match=match):
            deserializer.deserialize_data(d, objset)
    else:
        deserializer.deserialize_data(d, objset)


def test_node_kind_blank(model, test_context_url):
    s = model.JSONLDSerializer()
    c1 = model.link_class()
    c2 = model.link_class()

    c1._id = "http://example.com/c1"
    c2._id = "http://example.com/c2"

    ref = model.node_kind_blank()

    with pytest.raises(model.ValidationError):
        ref._id = "http://example.com/name"

    # Blank node assignment is fine but not preserved when serializing
    ref._id = "_:blank"

    # No blank ID is written out for one reference (inline)
    c1.link_class_link_prop = ref
    result = s.serialize_data(model.SHACLObjectSet([c1, c2]))
    assert result == {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "link-class",
                "@id": "http://example.com/c1",
                "link-class-link-prop": {
                    "@type": "node-kind-blank",
                },
            },
            {
                "@type": "link-class",
                "@id": "http://example.com/c2",
            },
        ],
    }

    # Blank node is written out for multiple references
    c2.link_class_link_prop = ref
    result = s.serialize_data(model.SHACLObjectSet([c1, c2]))
    assert result == {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "node-kind-blank",
                "@id": "_:node_kind_blank0",
            },
            {
                "@type": "link-class",
                "@id": "http://example.com/c1",
                "link-class-link-prop": "_:node_kind_blank0",
            },
            {
                "@type": "link-class",
                "@id": "http://example.com/c2",
                "link-class-link-prop": "_:node_kind_blank0",
            },
        ],
    }

    # Listing in the root graph requires a blank node be written
    result = s.serialize_data(model.SHACLObjectSet([c1, ref]))
    assert result == {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "node-kind-blank",
                "@id": "_:node_kind_blank0",
            },
            {
                "@type": "link-class",
                "@id": "http://example.com/c1",
                "link-class-link-prop": "_:node_kind_blank0",
            },
        ],
    }


@pytest.mark.parametrize(
    "cls",
    ["node_kind_iri", "derived_node_kind_iri"],
)
def test_node_kind_iri(model, test_context_url, cls):
    TEST_ID = "http://serialize.example.com/name"
    TYP = cls.replace("_", "-")

    s = model.JSONLDSerializer()
    c1 = model.link_class()
    c2 = model.link_class()

    c1._id = "http://example.com/c1"
    c2._id = "http://example.com/c2"

    ref = getattr(model, cls)()

    with pytest.raises(model.ValidationError):
        ref._id = "_:blank"

    # serializing without an ID is not allowed
    with pytest.raises(model.EncodeError):
        s.serialize_data(model.SHACLObjectSet([ref]))

    # Inlining not allowed
    ref._id = TEST_ID

    c1.link_class_link_prop = ref
    result = s.serialize_data(model.SHACLObjectSet([c1, c2]))
    assert result == {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "link-class",
                "@id": "http://example.com/c1",
                "link-class-link-prop": TEST_ID,
            },
            {
                "@type": "link-class",
                "@id": "http://example.com/c2",
            },
            {
                "@type": TYP,
                "@id": TEST_ID,
            },
        ],
    }

    # Multiple references
    c2.link_class_link_prop = ref
    result = s.serialize_data(model.SHACLObjectSet([c1, c2]))
    assert result == {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "link-class",
                "@id": "http://example.com/c1",
                "link-class-link-prop": TEST_ID,
            },
            {
                "@type": "link-class",
                "@id": "http://example.com/c2",
                "link-class-link-prop": TEST_ID,
            },
            {
                "@type": TYP,
                "@id": TEST_ID,
            },
        ],
    }

    # Listing in the root graph forces reference
    result = s.serialize_data(model.SHACLObjectSet([c1, ref]))
    assert result == {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "link-class",
                "@id": "http://example.com/c1",
                "link-class-link-prop": TEST_ID,
            },
            {
                "@type": TYP,
                "@id": TEST_ID,
            },
        ],
    }


@pytest.mark.parametrize(
    "cls",
    ["id_prop_class", "inherited_id_prop_class"],
)
def test_id_name(model, test_context_url, cls):
    """
    Test that alternate ID property names work correctly,
    including serialization and initialization.
    """

    s = model.JSONLDSerializer()
    c = getattr(model, cls)()

    TEST_ID = "http://serialize.example.com/name"

    # Assign alternate ID
    c.testid = TEST_ID
    assert c.testid == TEST_ID

    # alternate ID is an alias for the _id property
    assert c._id == TEST_ID

    # Delete id
    del c.testid
    assert c.testid is None
    assert c._id is None

    # Serialization should use the alias name
    c._id = TEST_ID
    result = s.serialize_data(model.SHACLObjectSet([c]))
    assert result == {
        "@context": test_context_url,
        "@type": cls.replace("_", "-"),
        "testid": TEST_ID,
    }

    # Test initialization using ID alias
    c2 = getattr(model, cls)(testid=TEST_ID)
    assert c2.get_id() == TEST_ID
    assert c2.testid == TEST_ID


def test_get_id_none(model):
    """get_id returns None when no ID is set."""
    c = model.test_class()
    assert c.get_id() is None


def test_get_id_set(model):
    """get_id returns the assigned IRI."""
    c = model.test_class()
    c._id = "http://example.com/obj"
    assert c.get_id() == "http://example.com/obj"


def test_set_id(model):
    """set_id assigns the IRI."""
    c = model.test_class()
    c.set_id("http://example.com/obj")
    assert c._id == "http://example.com/obj"
    assert c.get_id() == "http://example.com/obj"


def test_set_id_none(model):
    """set_id(None) clears the ID."""
    c = model.test_class()
    c.set_id("http://example.com/obj")
    c.set_id(None)
    assert c.get_id() is None
    assert c._id is None


def test_set_id_roundtrip(model, test_context_url):
    """Object serialized with set_id value encodes correct @id."""
    s = model.JSONLDSerializer()
    c = model.test_class()
    c.set_id("http://example.com/set-id-obj")
    result = s.serialize_data(model.SHACLObjectSet([c]))
    assert result["@id"] == "http://example.com/set-id-obj"


@pytest.mark.parametrize("cls", ["id_prop_class", "inherited_id_prop_class"])
def test_get_id_with_alias(model, cls):
    """get_id returns ID set via alias property."""
    # id-prop-class is a class with an ID alias "testid"
    c = getattr(model, cls)()
    c.testid = "http://example.com/alias-obj"
    assert c.get_id() == "http://example.com/alias-obj"


@pytest.mark.parametrize("cls", ["id_prop_class", "inherited_id_prop_class"])
def test_set_id_with_alias(model, cls):
    """set_id makes ID accessible through alias property."""
    # id-prop-class is a class with an ID alias "testid"
    c = getattr(model, cls)()
    c.set_id("http://example.com/alias-obj")
    assert c.testid == "http://example.com/alias-obj"
    assert c.get_id() == "http://example.com/alias-obj"


SAME_AS_VALUE = object()


def type_tests(name, *typ):
    tests = [
        (name, None, VALIDATION_ERROR),
        (name, [], VALIDATION_ERROR),
        (name, object(), VALIDATION_ERROR),
        (name, lambda model: sum, VALIDATION_ERROR),
    ]
    if bool not in typ and int not in typ:
        tests.append((name, True, VALIDATION_ERROR))
        tests.append((name, False, VALIDATION_ERROR))

    if int not in typ:
        tests.append((name, 1, VALIDATION_ERROR))

    if float not in typ:
        tests.append((name, 1.0, VALIDATION_ERROR))

    if datetime not in typ:
        tests.append((name, datetime(2024, 3, 11, 0, 0, 0), VALIDATION_ERROR)),

    if str not in typ:
        tests.append((name, "foo", VALIDATION_ERROR))

    return tests


@pytest.mark.parametrize(
    "prop,value,expect",
    [
        # positive integer
        ("test_class_positive_integer_prop", -1, VALIDATION_ERROR),
        ("test_class_positive_integer_prop", 0, VALIDATION_ERROR),
        ("test_class_positive_integer_prop", 1, 1),
        ("test_class_positive_integer_prop", False, VALIDATION_ERROR),
        ("test_class_positive_integer_prop", True, 1),
        *type_tests("test_class_positive_integer_prop", int),
        # non-negative integer
        ("test_class_nonnegative_integer_prop", -1, VALIDATION_ERROR),
        ("test_class_nonnegative_integer_prop", 0, 0),
        ("test_class_nonnegative_integer_prop", 1, 1),
        ("test_class_nonnegative_integer_prop", False, 0),
        ("test_class_nonnegative_integer_prop", True, 1),
        *type_tests("test_class_nonnegative_integer_prop", int),
        # integer
        ("test_class_integer_prop", -1, -1),
        ("test_class_integer_prop", 0, 0),
        ("test_class_integer_prop", 1, 1),
        ("test_class_integer_prop", False, 0),
        ("test_class_integer_prop", True, 1),
        *type_tests("test_class_integer_prop", int),
        # float
        ("test_class_float_prop", -1, -1.0),
        ("test_class_float_prop", -1.0, -1.0),
        ("test_class_float_prop", 0, 0.0),
        ("test_class_float_prop", 0.0, 0.0),
        ("test_class_float_prop", 1, 1.0),
        ("test_class_float_prop", 1.0, 1.0),
        ("test_class_float_prop", False, 0.0),
        ("test_class_float_prop", True, 1.0),
        *type_tests("test_class_float_prop", int, float),
        # boolean
        ("test_class_boolean_prop", True, True),
        ("test_class_boolean_prop", False, False),
        *type_tests("test_class_boolean_prop", bool),
        # datetime
        (
            # Local time
            "test_class_datetime_scalar_prop",
            lambda _: datetime(2024, 3, 11, 0, 0, 0),
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=TEST_TZ),
        ),
        (
            # Explicit timezone
            "test_class_datetime_scalar_prop",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(-timedelta(hours=6))),
            SAME_AS_VALUE,
        ),
        (
            # Explicit timezone
            "test_class_datetime_scalar_prop",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=0))),
            SAME_AS_VALUE,
        ),
        (
            "test_class_datetime_scalar_prop",
            # UTC
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            SAME_AS_VALUE,
        ),
        (
            "test_class_datetime_scalar_prop",
            # Microseconds are ignored
            lambda _: datetime(2024, 3, 11, 0, 0, 0, 999),
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=TEST_TZ),
        ),
        (
            "test_class_datetime_scalar_prop",
            # Minutes timezone
            datetime(
                2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=-1, minutes=21))
            ),
            SAME_AS_VALUE,
        ),
        (
            "test_class_datetime_scalar_prop",
            # Seconds from timezone are dropped
            datetime(
                2024,
                3,
                11,
                0,
                0,
                0,
                tzinfo=timezone(timedelta(hours=-1, minutes=-21, seconds=-31)),
            ),
            datetime(
                2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=-1, minutes=-21))
            ),
        ),
        *type_tests("test_class_datetime_scalar_prop", datetime),
        # datetimestamp
        (
            # Local time
            "test_class_datetimestamp_scalar_prop",
            lambda _: datetime(2024, 3, 11, 0, 0, 0),
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=TEST_TZ),
        ),
        (
            # Explicit timezone
            "test_class_datetimestamp_scalar_prop",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(-timedelta(hours=6))),
            SAME_AS_VALUE,
        ),
        (
            # Explicit timezone
            "test_class_datetimestamp_scalar_prop",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=0))),
            SAME_AS_VALUE,
        ),
        (
            "test_class_datetimestamp_scalar_prop",
            # UTC
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            SAME_AS_VALUE,
        ),
        (
            "test_class_datetimestamp_scalar_prop",
            # Microseconds are ignored
            datetime(2024, 3, 11, 0, 0, 0, 999, tzinfo=timezone.utc),
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
        ),
        (
            "test_class_datetimestamp_scalar_prop",
            # Minutes timezone
            datetime(
                2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=-1, minutes=21))
            ),
            SAME_AS_VALUE,
        ),
        (
            "test_class_datetimestamp_scalar_prop",
            # Seconds from timezone are dropped
            datetime(
                2024,
                3,
                11,
                0,
                0,
                0,
                tzinfo=timezone(timedelta(hours=-1, minutes=-21, seconds=-31)),
            ),
            datetime(
                2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=-1, minutes=-21))
            ),
        ),
        *type_tests("test_class_datetimestamp_scalar_prop", datetime),
        # String
        ("test_class_string_scalar_prop", "foo", "foo"),
        ("test_class_string_scalar_prop", "", ""),
        *type_tests("test_class_string_scalar_prop", str),
        # Named property
        ("named_property", "foo", "foo"),
        ("named_property", "", ""),
        *type_tests("named_property", str),
        # Enumerated value
        (
            "test_class_enum_prop",
            "http://example.org/shacl2code-test/enumType/foo",
            "http://example.org/shacl2code-test/enumType/foo",
        ),
        ("test_class_enum_prop", "foo", VALIDATION_ERROR),
        *type_tests("test_class_enum_prop", str),
        # Object
        ("test_class_class_prop", lambda model: model.test_class(), SAME_AS_VALUE),
        (
            "test_class_class_prop",
            lambda model: model.test_derived_class(),
            SAME_AS_VALUE,
        ),
        (
            "test_class_class_prop",
            lambda model: model.test_another_class(),
            VALIDATION_ERROR,
        ),
        ("test_class_class_prop", lambda model: model.parent_class(), VALIDATION_ERROR),
        ("test_class_class_prop", lambda model: model.test_class.named, SAME_AS_VALUE),
        ("test_class_class_prop", "_:blanknode", "_:blanknode"),
        (
            "test_class_class_prop",
            "http://serialize.example.org/test",
            "http://serialize.example.org/test",
        ),
        *type_tests("test_class_class_prop", str),
        # Pattern validated string
        ("test_class_regex", "foo1", "foo1"),
        ("test_class_regex", "foo2", "foo2"),
        ("test_class_regex", "foo2a", "foo2a"),
        ("test_class_regex", "bar", VALIDATION_ERROR),
        ("test_class_regex", "fooa", VALIDATION_ERROR),
        ("test_class_regex", "afoo1", VALIDATION_ERROR),
        *type_tests("test_class_regex", str),
        # Pattern validated dateTime
        (
            "test_class_regex_datetime",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=1))),
            SAME_AS_VALUE,
        ),
        (
            "test_class_regex_datetime",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(-timedelta(hours=6))),
            VALIDATION_ERROR,
        ),
        (
            "test_class_regex_datetime",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            VALIDATION_ERROR,
        ),
        (
            "test_class_regex_datetime",
            datetime(2024, 3, 11, 0, 0, 0),
            VALIDATION_ERROR,
        ),
        # Pattern validated dateTimeStamp
        (
            "test_class_regex_datetimestamp",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(-timedelta(hours=6))),
            VALIDATION_ERROR,
        ),
        (
            "test_class_regex_datetimestamp",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=0))),
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
        ),
        (
            "test_class_regex_datetimestamp",
            datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            SAME_AS_VALUE,
        ),
        # Property that is a keyword
        ("import_", "foo", "foo"),
        # A property that conflicts with an existing attribute
        ("encode_", "foo", "foo"),
        # Verify that existing attributes cannot be overwritten
        ("encode", "foo", AttributeError),
    ],
)
def test_scalar_prop_validation(model, test_timezone, prop, value, expect):
    c = model.test_class()

    if callable(value):
        value = value(model)

    if expect is SAME_AS_VALUE:
        expect = value

    kwargs = {prop: value}

    for cls in model.test_class, model.test_derived_class:
        c = cls()

        if expect is VALIDATION_ERROR:
            expect = model.ValidationError

        if isinstance(expect, type) and issubclass(expect, Exception):
            with pytest.raises(expect):
                setattr(c, prop, value)

            with pytest.raises(expect):
                c = cls(**kwargs)
        else:
            setattr(c, prop, value)
            assert getattr(c, prop) == expect
            assert type(getattr(c, prop)) is type(expect)

            c = cls(**kwargs)
            assert getattr(c, prop) == expect
            assert type(getattr(c, prop)) is type(expect)


def test_derived_property(model):
    # The test above covers most of the test cases with setting properties, but
    # it doesn't cover if the property is defined in the derived class, so test
    # those here
    c = model.test_derived_class(test_derived_class_string_prop="abc")
    assert c.test_derived_class_string_prop == "abc"

    c.test_derived_class_string_prop = "def"
    assert c.test_derived_class_string_prop == "def"


def list_type_tests(name, *typ):
    tests = [
        # Non list types
        (name, 1, VALIDATION_ERROR),
        (name, 1.0, VALIDATION_ERROR),
        (name, True, VALIDATION_ERROR),
        (name, "foo", VALIDATION_ERROR),
        (name, datetime(2024, 3, 11, 0, 0, 0), VALIDATION_ERROR),
        (name, object(), VALIDATION_ERROR),
        (name, [object()], VALIDATION_ERROR),
        (name, lambda model: sum, VALIDATION_ERROR),
        (name, [sum], VALIDATION_ERROR),
        # Empty list is always allowed
        (name, [], []),
    ]

    if bool not in typ and int not in typ:
        tests.append((name, [True], VALIDATION_ERROR))
        tests.append((name, [False], VALIDATION_ERROR))

    if int not in typ:
        tests.append((name, [1], VALIDATION_ERROR))

    if float not in typ:
        tests.append((name, [1.0], VALIDATION_ERROR))

    if datetime not in typ:
        tests.append((name, [datetime(2024, 3, 11, 0, 0, 0)], VALIDATION_ERROR)),

    if str not in typ:
        tests.append((name, ["foo"], VALIDATION_ERROR))

    return tests


@pytest.mark.parametrize(
    "prop,value,expect",
    [
        # string
        ("test_class_string_list_prop", ["foo", "bar"], ["foo", "bar"]),
        ("test_class_string_list_prop", [""], [""]),
        *list_type_tests("test_class_string_list_prop", str),
        # datetime
        (
            "test_class_datetime_list_prop",
            [
                datetime(2024, 3, 11, 0, 0, 0),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(-timedelta(hours=6))),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=0))),
                datetime(2024, 3, 11, 0, 0, 0, 999, tzinfo=timezone.utc),
                datetime(
                    2024,
                    3,
                    11,
                    0,
                    0,
                    0,
                    tzinfo=timezone(timedelta(hours=-1, minutes=21)),
                ),
                datetime(
                    2024,
                    3,
                    11,
                    0,
                    0,
                    0,
                    tzinfo=timezone(timedelta(hours=-1, minutes=-21, seconds=-31)),
                ),
            ],
            [
                datetime(2024, 3, 11, 0, 0, 0).astimezone(),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone(-timedelta(hours=6))),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
                datetime(2024, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
                datetime(
                    2024,
                    3,
                    11,
                    0,
                    0,
                    0,
                    tzinfo=timezone(timedelta(hours=-1, minutes=21)),
                ),
                datetime(
                    2024,
                    3,
                    11,
                    0,
                    0,
                    0,
                    tzinfo=timezone(timedelta(hours=-1, minutes=-21)),
                ),
            ],
        ),
        *list_type_tests("test_class_datetime_list_prop", datetime),
        # Enumerate type
        (
            "test_class_enum_list_prop",
            [
                "http://example.org/shacl2code-test/enumType/foo",
                "http://example.org/shacl2code-test/enumType/bar",
                "http://example.org/shacl2code-test/enumType/nolabel",
            ],
            [
                "http://example.org/shacl2code-test/enumType/foo",
                "http://example.org/shacl2code-test/enumType/bar",
                "http://example.org/shacl2code-test/enumType/nolabel",
            ],
        ),
        (
            "test_class_enum_list_prop",
            [
                "http://example.org/shacl2code-test/enumType/foo",
                "foo",
            ],
            VALIDATION_ERROR,
        ),
        *list_type_tests("test_class_enum_list_prop", str),
        # Object
        (
            "test_class_class_list_prop",
            lambda model: [
                model.test_class(),
                model.test_derived_class(),
                "_:blanknode",
                "http://serialize.example.org/test",
                "http://serialize.example.org/test",
            ],
            SAME_AS_VALUE,
        ),
        (
            "test_class_class_list_prop",
            lambda model: [model.test_another_class()],
            VALIDATION_ERROR,
        ),
        (
            "test_class_class_list_prop",
            lambda model: [model.parent_class()],
            VALIDATION_ERROR,
        ),
        *list_type_tests("test_class_class_list_prop", str),
        # Pattern validated
        (
            "test_class_regex_list",
            [
                "foo1",
                "foo2",
                "foo2a",
            ],
            [
                "foo1",
                "foo2",
                "foo2a",
            ],
        ),
        ("test_class_regex_list", ["bar"], VALIDATION_ERROR),
        ("test_class_regex_list", ["fooa"], VALIDATION_ERROR),
        ("test_class_regex_list", ["afoo1"], VALIDATION_ERROR),
        *list_type_tests("test_class_regex_list", str),
        # TODO Add more list tests
    ],
)
def test_list_prop_validation(model, prop, value, expect):
    c = model.test_class()

    if callable(value):
        value = value(model)

    if expect is SAME_AS_VALUE:
        expect = value

    kwargs = {prop: value}
    for cls in model.test_class, model.test_derived_class:
        c = cls()

        if expect is VALIDATION_ERROR:
            expect = model.ValidationError

        if isinstance(expect, type) and issubclass(expect, Exception):
            with pytest.raises(expect):
                if value is list:
                    for v in value:
                        getattr(c, prop).append(v)
                else:
                    setattr(c, prop, value)

            with pytest.raises(expect):
                cls(**kwargs)

        else:
            for v in value:
                getattr(c, prop).append(v)

            assert getattr(c, prop) == expect
            for idx, v in enumerate(expect):
                assert getattr(c, prop)[idx] == v
                assert type(getattr(c, prop)[idx]) is type(v)

            setattr(c, prop, value[:])
            assert getattr(c, prop) == expect

            assert list(getattr(c, prop)) == expect

            getattr(c, prop).sort()
            assert getattr(c, prop) == list(sorted(expect))

            setattr(c, prop, [])
            getattr(c, prop).extend(value)
            assert getattr(c, prop) == expect

            setattr(c, prop, [])
            for v in value:
                getattr(c, prop).insert(0, v)
            assert getattr(c, prop) == list(reversed(expect))

            for v in expect:
                assert v in getattr(c, prop)

            c = cls(**kwargs)
            assert getattr(c, prop) == expect


@timetests.datetime_decode_tests()
def test_datetime_from_string(model, value, expect):
    p = model.DateTimeProp()
    path = model.DataPath()

    if expect is None:
        with pytest.raises(model.ValidationError):
            p.from_string(path, value)
    else:
        v = p.from_string(path, value)
        assert v == expect


@timetests.datetimestamp_decode_tests()
def test_datetimestamp_from_string(model, value, expect):
    p = model.DateTimeStampProp()
    path = model.DataPath()

    if expect is None:
        with pytest.raises(model.ValidationError):
            p.from_string(path, value)
    else:
        v = p.from_string(path, value)
        assert v == expect


@timetests.datetime_encode_tests()
def test_datetime_to_string(model, value, expect):
    p = model.DateTimeProp()
    path = model.DataPath()

    if expect is None:
        with pytest.raises(model.ValidationError):
            p.to_string(path, value)
    else:
        v = p.to_string(path, value)
        assert v == expect
        assert re.match(
            model.DateTimeProp.REGEX, v
        ), f"Value '{v}' does not match regex"


@pytest.mark.parametrize(
    "prop,serkey,value,expect",
    [
        (
            "extensible_class_property",
            "extensible-class/property",
            "foo",
            "foo",
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            "http://example.org/shacl2code-test/extensible-test-prop",
            "foo",
            AttributeError,
        ),
    ],
)
def test_extensible_prop(model, test_context_url, prop, serkey, value, expect):
    e = model.extensible_class(extensible_class_required="required")

    if isinstance(expect, type) and issubclass(expect, Exception):
        with pytest.raises(expect):
            setattr(e, prop, value)
    else:
        setattr(e, prop, value)
        assert getattr(e, prop, value) == expect

        s = model.JSONLDSerializer()
        objset = model.SHACLObjectSet()
        objset.add(e)

        data = s.serialize_data(objset)

        assert data == {
            "@context": test_context_url,
            "@type": "extensible-class",
            "extensible-class/required": "required",
            serkey: expect,
        }


@pytest.mark.parametrize(
    "iri,value,expect,ser_data,ser_expect",
    [
        (
            "extensible_class_property",
            "foo",
            KeyError,
            None,
            None,
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            "foo",
            SAME_AS_VALUE,
            ["foo"],
            ["foo"],
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            1,
            SAME_AS_VALUE,
            [1],
            [1],
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            1.123,
            SAME_AS_VALUE,
            [1.123],
            [1.123],
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            object(),
            SAME_AS_VALUE,
            ENCODE_ERROR,
            None,
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            [1, "foo", 1.123],
            SAME_AS_VALUE,
            [1, "foo", 1.123],
            [1, "foo", 1.123],
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            "1.10",
            SAME_AS_VALUE,
            ["1.10"],
            ["1.10"],
        ),
        (
            "http://example.org/shacl2code-test/extensible-test-prop",
            [object()],
            SAME_AS_VALUE,
            ENCODE_ERROR,
            None,
        ),
    ],
)
def test_extensible_iri(
    model, test_context_url, iri, value, expect, ser_data, ser_expect
):
    e = model.extensible_class(extensible_class_required="required")

    if expect is SAME_AS_VALUE:
        expect = value

    if ser_data is SAME_AS_VALUE:
        ser_data = value

    if ser_expect is SAME_AS_VALUE:
        ser_expect = value

    if isinstance(expect, type) and issubclass(expect, Exception):
        with pytest.raises(expect):
            e[iri] = value
    else:
        e[iri] = value
        assert e[iri] == expect
        assert (None, iri, None) in e.property_keys()

        s = model.JSONLDSerializer()
        objset = model.SHACLObjectSet()
        objset.add(e)

        if ser_data is VALIDATION_ERROR:
            ser_data = model.ValidationError
        elif ser_data is ENCODE_ERROR:
            ser_data = model.EncodeError

        if isinstance(ser_data, type) and issubclass(ser_data, Exception):
            with pytest.raises(ser_data):
                data = s.serialize_data(objset)
        else:
            data = s.serialize_data(objset)
            assert data == {
                "@context": test_context_url,
                "@type": "extensible-class",
                "extensible-class/required": "required",
                iri: ser_data,
            }

            objset = model.SHACLObjectSet()
            d = model.JSONLDDeserializer()
            d.deserialize_data(data, objset)

            e = objset.objects.pop()
            assert e[iri] == ser_expect

        del e[iri]
        with pytest.raises(KeyError):
            e[iri]


def test_extensible_deserialize(model, test_context_url):
    def deserialize_extension(ext_data):
        d = model.JSONLDDeserializer()
        objset = model.SHACLObjectSet()
        d.deserialize_data(
            {
                "@context": test_context_url,
                "@type": "link-class",
                "link-class-extensible": ext_data,
            },
            objset,
        )
        return objset

    class ClosedExtension(model.extensible_class):
        CLOSED = True
        TYPE = "http://example.org/shacl2code-test/closed-class"

    class OpenExtension(model.extensible_class):
        TYPE = "http://example.org/shacl2code-test/open-class"

    TEST_TYPE = "http://example.org/shacl2code-test/test-extensible"
    TEST_IRI = "http://example.org/shacl2code-test/test-key"
    TEST_ID = "http://example.org/shacl2code-test/test-id"

    objset = deserialize_extension(
        {
            "@type": TEST_TYPE,
            "@id": TEST_ID,
            TEST_IRI: "foo",
        }
    )
    obj = objset.find_by_id(TEST_ID)
    assert obj is not None
    assert isinstance(obj, model.extensible_class)

    assert (None, TEST_IRI, None) in obj.property_keys()
    assert obj[TEST_IRI] == "foo"
    assert obj.get_type() == TEST_TYPE
    assert obj.get_compact_type() is None

    with pytest.raises(model.DecodeError):
        deserialize_extension(
            {
                "@type": TEST_TYPE,
                "@id": TEST_ID,
                "not-an-iri": "foo",
            }
        )

    with pytest.raises(model.DecodeError):
        deserialize_extension(
            {
                "@type": TEST_TYPE,
                "@id": TEST_ID,
                "_:blank": "foo",
            }
        )

    objset = deserialize_extension(
        {
            "@type": "http://example.org/shacl2code-test/closed-class",
            "@id": TEST_ID,
        }
    )
    obj = objset.find_by_id(TEST_ID)
    assert obj is not None
    assert isinstance(obj, ClosedExtension)
    assert obj.get_type() == "http://example.org/shacl2code-test/closed-class"
    assert obj.get_compact_type() is None

    # Derived object is closed and cannot have arbitrary IRI assignment
    with pytest.raises(KeyError):
        obj[TEST_IRI] = "foo"

    objset = deserialize_extension(
        {
            "@type": "http://example.org/shacl2code-test/open-class",
            "@id": TEST_ID,
        }
    )
    obj = objset.find_by_id(TEST_ID)
    assert obj is not None
    assert isinstance(obj, OpenExtension)
    assert obj.get_type() == "http://example.org/shacl2code-test/open-class"
    assert obj.get_compact_type() is None

    # Derived object is open and can have arbitrary assignments
    obj[TEST_IRI] = "foo"


def test_enum_named_individuals(model):
    assert type(model.enumType.foo) is str
    assert model.enumType.foo == "http://example.org/shacl2code-test/enumType/foo"

    c = model.test_class()

    assert model.enumType.NAMED_INDIVIDUALS == {
        "foo": "http://example.org/shacl2code-test/enumType/foo",
        "bar": "http://example.org/shacl2code-test/enumType/bar",
        "nolabel": "http://example.org/shacl2code-test/enumType/nolabel",
    }

    for name, value in model.enumType.NAMED_INDIVIDUALS.items():
        c.test_class_enum_prop = value
        assert getattr(model.enumType, name) == value


def test_mandatory_properties(model, tmp_path):
    """
    Tests that property cardinality (e.g. min count & max count) is checked when
    writing out a file
    """
    s = model.JSONLDSerializer()
    outfile = tmp_path / "test.json"

    def base_obj():
        c = model.test_class_required()
        c.test_class_required_string_scalar_prop = "foo"
        c.test_class_required_string_list_prop = ["bar", "baz"]
        return c

    # First validate that the base object is actually valid
    c = base_obj()
    with outfile.open("wb") as f:
        s.write(model.SHACLObjectSet([c]), f)

    # Required scalar property
    c = base_obj()
    del c.test_class_required_string_scalar_prop
    with outfile.open("wb") as f:
        with pytest.raises(model.ValidationError):
            s.write(model.SHACLObjectSet([c]), f)

    # Array that is deleted
    c = base_obj()
    del c.test_class_required_string_list_prop
    with outfile.open("wb") as f:
        with pytest.raises(model.ValidationError):
            s.write(model.SHACLObjectSet([c]), f)

    # Array initialized to empty list
    c = base_obj()
    c.test_class_required_string_list_prop = []
    with outfile.open("wb") as f:
        with pytest.raises(model.ValidationError):
            s.write(model.SHACLObjectSet([c]), f)

    # Array with too many items
    c = base_obj()
    c.test_class_required_string_list_prop.append("too many")
    with outfile.open("wb") as f:
        with pytest.raises(model.ValidationError):
            s.write(model.SHACLObjectSet([c]), f)


def test_iri(model, roundtrip):
    doc = model.SHACLObjectSet()
    with roundtrip.open("r") as f:
        deserializer = model.JSONLDDeserializer()
        deserializer.read(f, doc)

    c = doc.find_by_id("http://serialize.example.com/test")
    assert isinstance(c, model.test_class)

    assert c._IRI["_id"] == "@id"
    assert (
        c._IRI["named_property"]
        == "http://example.org/shacl2code-test/test-class/named-property"
    )

    for name, iri in c._IRI.items():
        assert c[iri] == getattr(c, name)

    with pytest.raises(KeyError):
        c._IRI["foo"]

    assert "foo" not in c._IRI


def test_shacl(roundtrip):
    from rdflib import RDF, URIRef

    data = rdflib.Graph()
    data.parse(roundtrip)

    # We need to add the referenced non-shape object, otherwise SHACL will
    # complain it is missing
    data.add(
        (
            URIRef("http://serialize.example.com/non-shape"),
            RDF.type,
            URIRef("http://example.org/shacl2code-test/non-shape-class"),
        )
    )

    conforms, result_graph, result_text = pyshacl.validate(
        data,
        shacl_graph=str(TEST_MODEL),
        ont_graph=str(TEST_MODEL),
    )
    assert conforms, result_text


def test_single_register(model):
    # Ensures that class property registration is only called once
    assert model.test_class._NEEDS_REG
    c1 = model.test_class()
    assert not model.test_class._NEEDS_REG

    c2 = model.test_class()
    assert not model.test_class._NEEDS_REG

    c1.test_class_string_scalar_prop = "abc"
    c2.test_class_string_scalar_prop = "def"

    assert c1.test_class_string_scalar_prop == "abc"
    assert c2.test_class_string_scalar_prop == "def"

    assert model.test_derived_class._NEEDS_REG
    _ = model.test_derived_class()
    assert not model.test_derived_class._NEEDS_REG

    _ = model.test_derived_class()
    assert not model.test_derived_class._NEEDS_REG


def test_objset_foreach_type(model, roundtrip):
    objset = model.SHACLObjectSet()

    EXTENSION_ID = "http://example.org/shacl2code-test/custom-extension"

    class Extension(model.extensible_class):
        TYPE = "http://example.org/shacl2code-test/custom-extension-class"

    with roundtrip.open("r") as f:
        model.JSONLDDeserializer().read(f, objset)

    objset.add(Extension(_id=EXTENSION_ID))

    expect = set()

    expect.add(objset.find_by_id("http://serialize.example.com/test"))
    expect.add(objset.find_by_id("http://serialize.example.com/nested-parent"))
    expect.add(
        objset.find_by_id(
            "http://serialize.example.com/test-named-individual-reference"
        )
    )
    expect.add(
        objset.find_by_id(
            "http://serialize.example.com/nested-parent"
        ).test_class_class_prop
    )
    expect.add(objset.find_by_id("http://serialize.example.com/test-special-chars"))
    assert expect != {None}

    assert set(objset.foreach_type(model.test_class, match_subclass=False)) == expect
    assert set(objset.foreach_type("test-class", match_subclass=False)) == expect
    assert (
        set(
            objset.foreach_type(
                "http://example.org/shacl2code-test/test-class", match_subclass=False
            )
        )
        == expect
    )

    expect.add(objset.find_by_id("http://serialize.example.com/required"))
    expect.add(objset.find_by_id("http://serialize.example.com/test-derived"))
    assert expect != {None}

    assert set(objset.foreach_type(model.test_class, match_subclass=True)) == expect
    assert set(objset.foreach_type("test-class", match_subclass=True)) == expect
    assert (
        set(
            objset.foreach_type(
                "http://example.org/shacl2code-test/test-class", match_subclass=True
            )
        )
        == expect
    )

    expect = set()
    assert (
        set(objset.foreach_type(model.extensible_class, match_subclass=False)) == expect
    )
    assert set(objset.foreach_type("extensible-class", match_subclass=False)) == expect
    assert (
        set(
            objset.foreach_type(
                "http://example.org/shacl2code-test/extensible-class",
                match_subclass=False,
            )
        )
        == expect
    )

    expect.add(objset.find_by_id(EXTENSION_ID))
    assert expect != {None}

    assert (
        set(objset.foreach_type(model.extensible_class, match_subclass=True)) == expect
    )
    assert set(objset.foreach_type("extensible-class", match_subclass=True)) == expect
    assert (
        set(
            objset.foreach_type(
                "http://example.org/shacl2code-test/extensible-class",
                match_subclass=True,
            )
        )
        == expect
    )

    assert set(objset.foreach_type(Extension, match_subclass=False)) == expect
    assert (
        set(
            objset.foreach_type(
                "http://example.org/shacl2code-test/custom-extension-class",
                match_subclass=False,
            )
        )
        == expect
    )

    # Test that concrete classes derived from abstract classes can be iterated
    expect = set()
    assert (
        set(objset.foreach_type(model.abstract_class, match_subclass=False)) == expect
    )

    expect.add(objset.find_by_id("http://serialize.example.com/concrete-class"))
    assert expect != {None}
    assert set(objset.foreach_type(model.abstract_class, match_subclass=True)) == expect


def test_objset_remove(model):
    """
    Tests that removing an object from the object set works correctly
    """
    obj1 = model.test_class(_id="https://example.org/obj1")
    obj2 = model.test_class(_id="https://example.org/obj2")

    objset = model.SHACLObjectSet([obj1, obj2])
    assert obj1 in objset
    assert obj2 in objset

    objset.remove(obj1)

    assert obj1 not in objset
    assert obj2 in objset


def test_objset_remove_not_existing(model):
    """
    Tests that removing an object that is not in the object set does not
    raise an error. It should just do nothing silently.
    """
    obj = model.test_class(_id="https://example.org/obj")
    objset = model.SHACLObjectSet()

    objset.remove(obj)


def test_objset_remove_invalid_type(model):
    """
    Tests that removing an object that is not a SHACLObject raises a TypeError
    """
    objset = model.SHACLObjectSet()

    with pytest.raises(TypeError):
        objset.remove("not-a-shacl-object")


@pytest.mark.parametrize(
    "abstract,concrete",
    [
        ("abstract_class", "concrete_class"),
        ("abstract_spdx_class", "concrete_spdx_class"),
        ("abstract_sh_class", "concrete_sh_class"),
    ],
)
def test_abstract_classes(model, abstract, concrete):
    # Test that abstract classes cannot be implemented
    with pytest.raises(NotImplementedError):
        cls = getattr(model, abstract)
        cls()

    # Test that concrete classes derived from abstract classes can be
    # implemented
    cls = getattr(model, concrete)
    cls()


def test_required_abstract_class_property(model, tmp_path):
    # Test that a class with a required property that references an abstract
    # class can be instantiated
    c = model.required_abstract()
    assert c.required_abstract_abstract_class_prop is None

    outfile = tmp_path / "out.json"
    objset = model.SHACLObjectSet()
    objset.add(c)
    s = model.JSONLDSerializer()

    # Attempting to serialize without assigning the property should fail
    with outfile.open("wb") as f:
        with pytest.raises(model.ValidationError):
            s.write(objset, f, indent=4)

    # Assigning a concrete class should succeed and allow serialization
    c.required_abstract_abstract_class_prop = model.concrete_class()
    with outfile.open("wb") as f:
        s.write(objset, f, indent=4)

    # Deleting an abstract class property should return it to None
    del c.required_abstract_abstract_class_prop
    assert c.required_abstract_abstract_class_prop is None


def test_extensible_abstract_class(model):
    class Extension(model.extensible_abstract_class):
        TYPE = "http://example.org/shacl2code-test/custom-extension-class"

    # Test that an extensible abstract class cannot be created
    with pytest.raises(NotImplementedError):
        model.extensible_abstract_class()

    # Test that a class derived from an abstract extensible class can be
    # created
    Extension()


def test_named_individual(model, roundtrip):
    objset = model.SHACLObjectSet()
    with roundtrip.open("r") as f:
        d = model.JSONLDDeserializer()
        d.read(f, objset)

    c = objset.find_by_id(
        "http://serialize.example.com/test-named-individual-reference"
    )
    assert c is not None
    assert c.test_class_class_prop == model.test_class.named

    assert model.test_class.named not in objset.missing_ids


def test_missing_ids(model, roundtrip):
    objset = model.SHACLObjectSet()
    with roundtrip.open("r") as f:
        d = model.JSONLDDeserializer()
        d.read(f, objset)

    assert objset.missing_ids == {
        "http://serialize.example.com/non-shape",
    }


def test_deprecated_class(model):
    with pytest.deprecated_call():
        model.test_deprecated_class()


def test_deprecated_property(model):
    with pytest.warns(DeprecationWarning):
        c = model.test_deprecated_class()

    with pytest.deprecated_call():
        c.test_deprecated_class_deprecated_string_prop = "foo"


@jsonvalidation.context_tests()
def test_objset_context(model, context, expanded, compacted):
    objset = model.SHACLObjectSet()
    objset.context = context

    assert objset.compact_iri(expanded, expanded) == compacted
    assert expanded == objset.expand_iri(compacted, compacted)


def test_slots(model):
    assert model.model._USE_SLOTS


def test_slots_yes(tmp_path):
    output_dir = tmp_path / "output"
    shacl2code_generate(["--input", TEST_MODEL], ["--use-slots", "yes"], output_dir)
    text = (output_dir / "model.py").read_text()
    assert "_USE_SLOTS = True" in text


def test_slots_no(tmp_path):
    output_dir = tmp_path / "output"
    shacl2code_generate(["--input", TEST_MODEL], ["--use-slots", "no"], output_dir)
    text = (output_dir / "model.py").read_text()
    assert "_USE_SLOTS = False" in text


RESERVED_WORDS_MODEL = DATA_DIR / "reserved-words.ttl"


def test_varname_reserved_words(tmp_path):
    """
    varname() must append '_' to property names that collide with
    SHACLOBJECT_RESERVED_WORDS or Python keywords so that the generated
    ClassProp pyname, the __init__ kwargs, and _OBJ_PY_PROPS keys all agree.
    """
    output_dir = tmp_path / "temp_rwmodel"
    shacl2code_generate(["--input", RESERVED_WORDS_MODEL], [], output_dir)

    # Generated source must contain the renamed names, not the originals
    text = (output_dir / "model.py").read_text()
    for renamed in ("get_id_", "set_id_", "encode_", "class_"):
        assert (
            renamed in text
        ), f"expected renamed property '{renamed}' in generated code"
    for original in ('"get_id"', '"set_id"', '"encode"', '"class"'):
        assert (
            f"ClassProp({original}," not in text
        ), f"unrenamed property {original} found as ClassProp pyname"

    # Import the generated module and exercise the renamed properties
    old_path = sys.path[:]
    sys.path.append(str(tmp_path))
    try:
        import temp_rwmodel as m  # noqa: PLC0415

        cls = m.SHACLObject.CLASSES["http://example.org/shacl2code-test/test-rw-class"]

        # Renamed kwargs must work at construction time
        obj = cls(get_id_="a", set_id_="b", encode_="c", class_="d")
        assert obj.get_id_ == "a"
        assert obj.set_id_ == "b"
        assert obj.encode_ == "c"
        assert obj.class_ == "d"

        # SHACLObject.get_id() must still return the object IRI,
        # not the value of the prop (get_id_)
        assert obj.get_id() is None
        obj.set_id("http://example.org/shacl2code-test/obj")
        assert obj.get_id() == "http://example.org/shacl2code-test/obj"
    finally:
        sys.path = old_path
        for mod in list(sys.modules):
            if mod == "rwmodel" or mod.startswith("rwmodel."):
                del sys.modules[mod]


def test_extensible_properties(model, test_context_url):

    class Extension(model.extensible_class):
        TYPE = "http://example.org/shacl2code-test/extension"
        PROPERTIES = [
            model.ClassProp(
                "string_prop",
                lambda: model.StringProp(),
                "http://example.org/shacl2code-test/string-prop",
                min_count=1,
            ),
        ]

    DATA = {
        "@context": [
            test_context_url,
            {
                "prefix": "http://example.org/shacl2code-test/",
            },
        ],
        "@graph": [
            {
                "@type": "prefix:extension",
                "@id": "prefix:e",
                "prefix:string-prop": "foo",
                "extensible-class/required": "required",
                "prefix:extra-data": ["bar"],
            }
        ],
    }

    objset = model.SHACLObjectSet()
    d = model.JSONLDDeserializer()
    d.deserialize_data(DATA, objset)

    e = objset.find_by_id("http://example.org/shacl2code-test/e")
    assert e
    assert isinstance(e, Extension)
    assert e.string_prop == "foo"
    assert e["http://example.org/shacl2code-test/string-prop"] == "foo"
    assert e._id == "http://example.org/shacl2code-test/e"
    assert e["http://example.org/shacl2code-test/extra-data"] == ["bar"]

    # Ensure the context is preserved
    s = model.JSONLDSerializer()
    assert s.serialize_data(objset, True) == DATA


def test_extensible_value_objects(model, test_context_url, tmp_path):
    # JSON-LD node references and value objects in extensible properties
    # must round trip, as must native JSON values
    XSD_DECIMAL = "http://www.w3.org/2001/XMLSchema#decimal"
    PREFIX = "http://example.org/shacl2code-test/"

    DATA = {
        "@context": test_context_url,
        "@type": PREFIX + "test-extensible",
        "@id": PREFIX + "e",
        "extensible-class/required": "required",
        PREFIX + "iri-prop": {"@id": PREFIX + "iri-value"},
        PREFIX + "literal-prop": {"@value": "0.35", "@type": XSD_DECIMAL},
        PREFIX + "float-prop": 0.35,
        PREFIX + "string-prop": "1.10",
        PREFIX
        + "mixed-prop": [
            {"@id": PREFIX + "iri-value"},
            {"@value": "1.5", "@type": XSD_DECIMAL},
            1.5,
            "1.5",
            1,
            True,
        ],
    }

    objset = model.SHACLObjectSet()
    model.JSONLDDeserializer().deserialize_data(DATA, objset)

    e = objset.find_by_id(PREFIX + "e")
    assert isinstance(e, model.extensible_class)
    assert e[PREFIX + "iri-prop"] == model.IRIRef(PREFIX + "iri-value")
    assert e[PREFIX + "literal-prop"] == model.TypedLiteral("0.35", XSD_DECIMAL)
    assert e[PREFIX + "float-prop"] == 0.35
    assert e[PREFIX + "string-prop"] == "1.10"
    assert e[PREFIX + "mixed-prop"] == [
        model.IRIRef(PREFIX + "iri-value"),
        model.TypedLiteral("1.5", XSD_DECIMAL),
        1.5,
        "1.5",
        1,
        True,
    ]

    # Extensible properties are always written as lists
    expect = {
        k: [v] if k.startswith(PREFIX) and not isinstance(v, list) else v
        for k, v in DATA.items()
    }

    assert model.JSONLDSerializer().serialize_data(objset) == expect

    outfile = tmp_path / "out.json"
    with outfile.open("wb") as f:
        model.JSONLDInlineSerializer().write(objset, f)
    with outfile.open("r") as f:
        # The inline serializer always writes a @graph
        assert json.load(f) == {
            "@context": test_context_url,
            "@graph": [{k: v for k, v in expect.items() if k != "@context"}],
        }

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    subject = rdflib.URIRef(PREFIX + "e")
    assert g.value(subject, rdflib.URIRef(PREFIX + "iri-prop")) == rdflib.URIRef(
        PREFIX + "iri-value"
    )
    assert g.value(subject, rdflib.URIRef(PREFIX + "literal-prop")) == rdflib.Literal(
        "0.35", datatype=rdflib.URIRef(XSD_DECIMAL)
    )


EXT_PREFIX = "http://example.org/shacl2code-test/"
XSD = "http://www.w3.org/2001/XMLSchema#"
RDF_JSON = "http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON"


def ext_doc(context, **props):
    """Build a JSON-LD document with one extensible object"""
    d = {
        "@context": context,
        "@type": EXT_PREFIX + "test-extensible",
        "@id": EXT_PREFIX + "e",
        "extensible-class/required": "required",
    }
    d.update(props)
    return d


def ext_value(model, data):
    """Deserialize a JSON-LD document and return the extensible object"""
    objset = model.SHACLObjectSet()
    model.JSONLDDeserializer().deserialize_data(data, objset)
    e = objset.find_by_id(EXT_PREFIX + "e")
    assert isinstance(e, model.extensible_class)
    return objset, e


def strict_json_loads(s):
    def reject(c):
        raise ValueError(f"Invalid JSON constant {c}")

    return json.loads(s, parse_constant=reject)


def write_inline(model, objset, tmp_path):
    outfile = tmp_path / "out.json"
    with outfile.open("wb") as f:
        model.JSONLDInlineSerializer().write(objset, f)
    return outfile.read_text()


@pytest.mark.parametrize(
    "value",
    [
        pytest.param({"@id": 1}, id="non-string @id"),
        pytest.param({"@value": "1", "@type": 1}, id="non-string @type"),
        pytest.param({"@value": [1], "@type": XSD + "decimal"}, id="list @value"),
        pytest.param({"@value": 1, "@language": "en"}, id="non-string lang value"),
        pytest.param({"@value": "a", "@language": 1}, id="non-string language"),
        pytest.param(
            {"@value": "a", "@type": XSD + "string", "@language": "en"},
            id="@type and @language",
        ),
        pytest.param(
            {"@value": "a", "@language": "en", "@direction": "up"},
            id="bad @direction",
        ),
    ],
)
def test_extensible_value_objects_invalid(model, test_context_url, value):
    with pytest.raises(model.DecodeError):
        ext_value(model, ext_doc(test_context_url, **{EXT_PREFIX + "prop": value}))


@pytest.mark.parametrize(
    "value,match",
    [
        pytest.param({"@list": [1, 2]}, "@list", id="list object"),
        pytest.param({"@set": [1, 2]}, "@set", id="set object"),
        pytest.param(
            {"@type": [EXT_PREFIX + "a", EXT_PREFIX + "b"], EXT_PREFIX + "p": "v"},
            "node object",
            id="node object with several types",
        ),
        pytest.param(
            {"@value": "a", "@direction": "ltr"}, "@direction", id="direction only"
        ),
    ],
)
def test_extensible_value_objects_unsupported(model, test_context_url, value, match):
    # Unsupported JSON-LD forms can be read, but give a clear error naming
    # the form when written
    objset, e = ext_value(
        model, ext_doc(test_context_url, **{EXT_PREFIX + "prop": value})
    )
    with pytest.raises(model.EncodeError, match=match):
        model.JSONLDSerializer().serialize_data(objset)


def test_extensible_value_objects_rdf_roundtrip(model, test_context_url):
    # JSON-LD -> objects -> RDF -> objects -> JSON-LD must not lose data
    DATA = ext_doc(
        test_context_url,
        **{
            EXT_PREFIX + "iri-prop": {"@id": EXT_PREFIX + "iri-value"},
            EXT_PREFIX + "bnode-prop": {"@id": "_:blank"},
            EXT_PREFIX + "decimal-prop": {"@value": "0.350", "@type": XSD + "decimal"},
            EXT_PREFIX + "double-prop": 0.35,
            EXT_PREFIX + "integral-double-prop": 1.0,
            EXT_PREFIX + "nan-prop": float("nan"),
            EXT_PREFIX + "int-prop": 1,
            EXT_PREFIX + "bool-prop": True,
            EXT_PREFIX + "string-prop": "1.10",
            EXT_PREFIX + "lang-prop": {"@value": "chat", "@language": "fr"},
            EXT_PREFIX
            + "json-prop": {"@value": {"b": [1, 2], "a": None}, "@type": "@json"},
            EXT_PREFIX
            + "multi-iri-prop": [
                {"@id": EXT_PREFIX + "iri-value"},
                # Reference to an object that is itself in the graph
                {"@id": EXT_PREFIX + "e"},
            ],
        },
    )

    objset, e = ext_value(model, DATA)
    expect = model.JSONLDSerializer().serialize_data(objset)

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)

    subject = rdflib.URIRef(EXT_PREFIX + "e")
    assert isinstance(
        g.value(subject, rdflib.URIRef(EXT_PREFIX + "bnode-prop")), rdflib.BNode
    )
    assert g.value(subject, rdflib.URIRef(EXT_PREFIX + "nan-prop")) == rdflib.Literal(
        "NaN", datatype=rdflib.XSD.double, normalize=False
    )
    assert g.value(subject, rdflib.URIRef(EXT_PREFIX + "lang-prop")) == rdflib.Literal(
        "chat", lang="fr"
    )

    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    e2 = objset2.find_by_id(EXT_PREFIX + "e")
    assert e2[EXT_PREFIX + "iri-prop"] == model.IRIRef(EXT_PREFIX + "iri-value")
    assert e2[EXT_PREFIX + "bnode-prop"] == model.IRIRef("_:blank")
    assert e2[EXT_PREFIX + "decimal-prop"] == model.TypedLiteral(
        "0.350", XSD + "decimal"
    )
    assert e2[EXT_PREFIX + "double-prop"] == 0.35
    assert isinstance(e2[EXT_PREFIX + "integral-double-prop"], float)
    assert e2[EXT_PREFIX + "int-prop"] == 1
    assert e2[EXT_PREFIX + "bool-prop"] is True
    assert e2[EXT_PREFIX + "lang-prop"] == model.LangString("chat", "fr")

    actual = model.JSONLDSerializer().serialize_data(objset2)

    # RDF does not preserve the order of multiple values
    for d in (expect, actual):
        d[EXT_PREFIX + "multi-iri-prop"].sort(key=lambda v: v["@id"])

    assert actual == expect


def sort_lists(v):
    """Sort all lists in a JSON value, as RDF does not preserve value order"""
    if isinstance(v, dict):
        return {k: sort_lists(i) for k, i in v.items()}
    if isinstance(v, list):
        return sorted(
            (sort_lists(i) for i in v), key=lambda i: json.dumps(i, sort_keys=True)
        )
    return v


NODE_DATA_PROPS = {
    # A list of several node objects, as in SPDX custom extensions
    EXT_PREFIX
    + "metric": [
        {
            "@type": EXT_PREFIX + "Metric",
            EXT_PREFIX + "name": "accuracy",
            EXT_PREFIX + "value": {"@value": "0.91", "@type": XSD + "decimal"},
        },
        {
            "@type": EXT_PREFIX + "Metric",
            EXT_PREFIX + "name": "f1",
            EXT_PREFIX + "value": {"@value": "0.88", "@type": XSD + "decimal"},
        },
    ],
    # A node object with an IRI and nested node objects, two levels deep
    EXT_PREFIX
    + "run": {
        "@type": EXT_PREFIX + "Run",
        "@id": EXT_PREFIX + "run-1",
        EXT_PREFIX + "label": {"@value": "essai", "@language": "fr"},
        EXT_PREFIX + "ref": {"@id": EXT_PREFIX + "iri-value"},
        EXT_PREFIX
        + "step": {
            EXT_PREFIX + "count": 3,
            EXT_PREFIX
            + "detail": {"@type": EXT_PREFIX + "Detail", EXT_PREFIX + "ok": True},
        },
    },
}


def node_data_expect(data):
    """The JSON-LD the serializer writes for NODE_DATA_PROPS"""

    def as_lists(v):
        if isinstance(v, list):
            return [as_lists(i) for i in v]
        if isinstance(v, dict) and "@value" not in v and set(v) - {"@id"}:
            return {
                k: (
                    i
                    if k.startswith("@")
                    else as_lists(i if isinstance(i, list) else [i])
                )
                for k, i in v.items()
            }
        return v

    return {
        k: (
            as_lists(v if isinstance(v, list) else [v])
            if k.startswith(EXT_PREFIX)
            else v
        )
        for k, v in data.items()
    }


def test_extensible_node_object(model, test_context_url, tmp_path):
    # Embedded node objects of types that are not in the model are read as
    # NodeObject, with their property values read by the same rules as
    # extensible properties
    DATA = ext_doc(test_context_url, **NODE_DATA_PROPS)
    objset, e = ext_value(model, DATA)

    assert e[EXT_PREFIX + "metric"] == [
        model.NodeObject(
            EXT_PREFIX + "Metric",
            properties={
                EXT_PREFIX + "name": "accuracy",
                EXT_PREFIX + "value": model.TypedLiteral("0.91", XSD + "decimal"),
            },
        ),
        model.NodeObject(
            EXT_PREFIX + "Metric",
            properties={
                EXT_PREFIX + "name": "f1",
                EXT_PREFIX + "value": model.TypedLiteral("0.88", XSD + "decimal"),
            },
        ),
    ]
    run = e[EXT_PREFIX + "run"]
    assert isinstance(run, model.NodeObject)
    assert run.type == EXT_PREFIX + "Run"
    assert run.id == EXT_PREFIX + "run-1"
    assert run.properties[EXT_PREFIX + "label"] == model.LangString("essai", "fr")
    assert run.properties[EXT_PREFIX + "ref"] == model.IRIRef(EXT_PREFIX + "iri-value")
    step = run.properties[EXT_PREFIX + "step"]
    assert step == model.NodeObject(
        properties={
            EXT_PREFIX + "count": 3,
            EXT_PREFIX
            + "detail": model.NodeObject(
                EXT_PREFIX + "Detail", properties={EXT_PREFIX + "ok": True}
            ),
        }
    )
    # Node objects are values, so are not objects of the object set
    assert len(objset.objects) == 1
    assert objset.find_by_id(EXT_PREFIX + "run-1") is None

    expect = node_data_expect(DATA)
    assert model.JSONLDSerializer().serialize_data(objset) == expect

    assert json.loads(write_inline(model, objset, tmp_path)) == {
        "@context": test_context_url,
        "@graph": [{k: v for k, v in expect.items() if k != "@context"}],
    }


def test_extensible_node_object_rdf_roundtrip(model, test_context_url):
    # JSON-LD -> objects -> RDF -> objects -> JSON-LD must not lose data
    DATA = ext_doc(test_context_url, **NODE_DATA_PROPS)
    objset, e = ext_value(model, DATA)
    expect = model.JSONLDSerializer().serialize_data(objset)

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)

    subject = rdflib.URIRef(EXT_PREFIX + "e")
    metrics = list(g.objects(subject, rdflib.URIRef(EXT_PREFIX + "metric")))
    assert len(metrics) == 2
    for m in metrics:
        assert isinstance(m, rdflib.BNode)
        assert g.value(m, rdflib.RDF.type) == rdflib.URIRef(EXT_PREFIX + "Metric")
    run = g.value(subject, rdflib.URIRef(EXT_PREFIX + "run"))
    assert run == rdflib.URIRef(EXT_PREFIX + "run-1")
    assert g.value(run, rdflib.URIRef(EXT_PREFIX + "label")) == rdflib.Literal(
        "essai", lang="fr"
    )

    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    # Node objects must not also be read as top-level objects
    assert len(objset2.objects) == 1
    e2 = objset2.find_by_id(EXT_PREFIX + "e")
    run2 = e2[EXT_PREFIX + "run"]
    assert isinstance(run2, model.NodeObject)
    assert run2.id == EXT_PREFIX + "run-1"
    # A blank node referenced only once has no identifier
    assert all(m.id is None for m in e2[EXT_PREFIX + "metric"])

    actual = model.JSONLDSerializer().serialize_data(objset2)
    assert sort_lists(actual) == sort_lists(expect)


def test_extensible_node_object_iri_reference(model, test_context_url):
    # An IRI without properties of its own is still a node reference in RDF
    DATA = ext_doc(
        test_context_url,
        **{EXT_PREFIX + "ref": {"@id": EXT_PREFIX + "iri-value"}},
    )
    objset, e = ext_value(model, DATA)
    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    e2 = objset2.find_by_id(EXT_PREFIX + "e")
    assert e2[EXT_PREFIX + "ref"] == model.IRIRef(EXT_PREFIX + "iri-value")


def test_extensible_node_object_shared_blank_node(model, test_context_url):
    # A blank node referenced more than once keeps its identifier, so that
    # it is still the same node when written back
    objset, e = ext_value(
        model,
        ext_doc(
            test_context_url,
            **{
                EXT_PREFIX
                + "a": {
                    "@id": "_:shared",
                    "@type": EXT_PREFIX + "T",
                    EXT_PREFIX + "p": "v",
                },
                EXT_PREFIX + "b": {"@id": "_:shared"},
            },
        ),
    )
    assert e[EXT_PREFIX + "a"].id == "_:shared"

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    subject = rdflib.URIRef(EXT_PREFIX + "e")
    a = g.value(subject, rdflib.URIRef(EXT_PREFIX + "a"))
    assert isinstance(a, rdflib.BNode)
    assert g.value(subject, rdflib.URIRef(EXT_PREFIX + "b")) == a

    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    assert len(objset2.objects) == 1
    e2 = objset2.find_by_id(EXT_PREFIX + "e")
    a2 = e2[EXT_PREFIX + "a"]
    b2 = e2[EXT_PREFIX + "b"]
    assert isinstance(a2, model.NodeObject)
    assert a2.id and a2.id.startswith("_:")
    assert a2 == b2

    g2 = rdflib.Graph()
    model.RDFSerializer().write(objset2, g2)
    assert len(g2) == len(g)


def test_extensible_node_object_context(model, test_context_url):
    # Types and property keys of node objects are expanded and compacted
    # with the context, as for other objects
    CONTEXT = [test_context_url, {"ex": EXT_PREFIX}]
    DATA = ext_doc(
        CONTEXT,
        **{
            "ex:node": [
                {"@type": "ex:T", "@id": "ex:n", "ex:p": "v"},
            ],
        },
    )
    objset, e = ext_value(model, DATA)
    assert e[EXT_PREFIX + "node"] == [
        model.NodeObject(EXT_PREFIX + "T", EXT_PREFIX + "n", {EXT_PREFIX + "p": "v"})
    ]
    data = model.JSONLDSerializer().serialize_data(objset)
    assert data["ex:node"] == [{"@type": "ex:T", "@id": "ex:n", "ex:p": ["v"]}]


def test_extensible_node_object_create(model, tmp_path):
    # A NodeObject can be created and written
    e = model.extensible_class(extensible_class_required="required")
    node = model.NodeObject(
        EXT_PREFIX + "T",
        properties={
            EXT_PREFIX + "p": ["a", model.NodeObject(properties={EXT_PREFIX + "q": 1})]
        },
    )
    e[EXT_PREFIX + "prop"] = node
    objset = model.SHACLObjectSet()
    objset.add(e)

    expect = [
        {
            "@type": EXT_PREFIX + "T",
            EXT_PREFIX + "p": ["a", {EXT_PREFIX + "q": [1]}],
        }
    ]
    assert (
        model.JSONLDSerializer().serialize_data(objset)[EXT_PREFIX + "prop"] == expect
    )
    assert (
        json.loads(write_inline(model, objset, tmp_path))["@graph"][0][
            EXT_PREFIX + "prop"
        ]
        == expect
    )

    # Values with equal content are equal and hash the same
    assert node == model.NodeObject(
        EXT_PREFIX + "T",
        properties={
            EXT_PREFIX + "p": ["a", model.NodeObject(properties={EXT_PREFIX + "q": 1})]
        },
    )
    assert hash(node) == hash(model.NodeObject(EXT_PREFIX + "T"))
    with pytest.raises(TypeError):
        model.NodeObject(1)
    with pytest.raises(TypeError):
        model.NodeObject(properties=[])


def test_extensible_node_object_known_type(model, test_context_url, tmp_path):
    # An embedded node object whose type is a class of the model is read as
    # an object of that class
    DATA = ext_doc(
        test_context_url,
        **{
            EXT_PREFIX
            + "obj": [
                {
                    "@type": "test-class",
                    "test-class/string-scalar-prop": "nested",
                },
            ],
        },
    )
    objset, e = ext_value(model, DATA)
    (obj,) = e[EXT_PREFIX + "obj"]
    assert isinstance(obj, model.test_class)
    assert obj.test_class_string_scalar_prop == "nested"
    assert obj in set(objset.foreach())

    data = model.JSONLDSerializer().serialize_data(objset)
    assert data == DATA
    assert json.loads(write_inline(model, objset, tmp_path))["@graph"] == [
        {k: v for k, v in DATA.items() if k != "@context"}
    ]

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    # The blank node must stay inline, not also be a top-level object
    assert len(objset2.objects) == 1
    e2 = objset2.find_by_id(EXT_PREFIX + "e")
    (obj2,) = (
        e2[EXT_PREFIX + "obj"]
        if isinstance(e2[EXT_PREFIX + "obj"], list)
        else [e2[EXT_PREFIX + "obj"]]
    )
    assert isinstance(obj2, model.test_class)
    assert model.JSONLDSerializer().serialize_data(objset2) == DATA


def test_extensible_node_object_keyword_aliases(alias_model):
    model = alias_model
    DATA = {
        "@context": ALIAS_CONTEXT_URL,
        "type": EXT_PREFIX + "test-extensible",
        "@id": EXT_PREFIX + "e",
        "extensible-class/required": "required",
        EXT_PREFIX
        + "node": {
            "type": EXT_PREFIX + "T",
            "spdxId": EXT_PREFIX + "n",
            EXT_PREFIX + "p": {"@value": "1.0", "type": XSD + "decimal"},
        },
    }
    objset = model.SHACLObjectSet()
    model.JSONLDDeserializer().deserialize_data(DATA, objset)
    (e,) = objset.objects
    assert e[EXT_PREFIX + "node"] == model.NodeObject(
        EXT_PREFIX + "T",
        EXT_PREFIX + "n",
        {EXT_PREFIX + "p": model.TypedLiteral("1.0", XSD + "decimal")},
    )
    data = model.JSONLDSerializer().serialize_data(objset)
    assert data[EXT_PREFIX + "node"] == [
        {
            "type": EXT_PREFIX + "T",
            "@id": EXT_PREFIX + "n",
            EXT_PREFIX + "p": [{"@value": "1.0", "@type": XSD + "decimal"}],
        }
    ]


@pytest.mark.parametrize(
    "value,lexical",
    [
        (float("nan"), "NaN"),
        (float("inf"), "INF"),
        (float("-inf"), "-INF"),
    ],
)
def test_extensible_non_finite_float(model, test_context_url, tmp_path, value, lexical):
    e = model.extensible_class(extensible_class_required="required")
    e[EXT_PREFIX + "prop"] = value
    objset = model.SHACLObjectSet()
    objset.add(e)

    expect = [{"@value": lexical, "@type": XSD + "double"}]

    data = model.JSONLDSerializer().serialize_data(objset)
    assert data[EXT_PREFIX + "prop"] == expect
    # Must be valid (RFC 8259) JSON
    strict_json_loads(json.dumps(data, allow_nan=False))

    text = write_inline(model, objset, tmp_path)
    assert strict_json_loads(text)["@graph"][0][EXT_PREFIX + "prop"] == expect

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    (o,) = g.objects(None, rdflib.URIRef(EXT_PREFIX + "prop"))
    assert str(o) == lexical
    assert o.datatype == rdflib.XSD.double

    # Read back as a float
    data["@id"] = EXT_PREFIX + "e"
    _, e2 = ext_value(model, data)
    (v,) = e2[EXT_PREFIX + "prop"]
    assert isinstance(v, float)
    assert repr(v) == repr(value)


def test_extensible_integral_float(model, test_context_url, tmp_path):
    # A float without a fractional part must not be written as a plain JSON
    # number, which JSON-LD reads as xsd:integer
    e = model.extensible_class(extensible_class_required="required")
    e[EXT_PREFIX + "prop"] = 1.0
    objset = model.SHACLObjectSet()
    objset.add(e)

    expect = [{"@value": 1.0, "@type": XSD + "double"}]
    data = model.JSONLDSerializer().serialize_data(objset)
    assert data[EXT_PREFIX + "prop"] == expect
    assert (
        strict_json_loads(write_inline(model, objset, tmp_path))["@graph"][0][
            EXT_PREFIX + "prop"
        ]
        == expect
    )

    for v in (
        {"@value": 1, "@type": XSD + "double"},
        {"@value": 1.0, "@type": XSD + "double"},
        {"@value": "1E0", "@type": XSD + "double"},
    ):
        _, e2 = ext_value(model, ext_doc(test_context_url, **{EXT_PREFIX + "prop": v}))
        assert e2[EXT_PREFIX + "prop"] == 1.0
        assert isinstance(e2[EXT_PREFIX + "prop"], float)


def test_extensible_iri_context(model, test_context_url):
    # Node reference IRIs are document-relative, so are never expanded or
    # compacted with a whole term, only with prefixes ending in a gen-delim
    CONTEXT = [
        test_context_url,
        {"foo": "https://ex.org/ns/foo", "ex": "https://ex.org/ns/"},
    ]
    DATA = ext_doc(
        CONTEXT,
        **{
            EXT_PREFIX + "term-id": {"@id": "foo"},
            EXT_PREFIX + "prefix-id": {"@id": "ex:bar"},
            EXT_PREFIX + "non-prefix-id": {"@id": "foo:bar"},
            EXT_PREFIX + "absolute-id": {"@id": "https://ex.org/ns/foo"},
            EXT_PREFIX + "term-type": {"@value": "x", "@type": "foo"},
            EXT_PREFIX + "prefix-type": {"@value": "x", "@type": "ex:bar"},
            EXT_PREFIX + "non-prefix-type": {"@value": "x", "@type": "foo:bar"},
        },
    )

    objset, e = ext_value(model, DATA)
    assert e[EXT_PREFIX + "term-id"] == model.IRIRef("foo")
    assert e[EXT_PREFIX + "prefix-id"] == model.IRIRef("https://ex.org/ns/bar")
    assert e[EXT_PREFIX + "non-prefix-id"] == model.IRIRef("foo:bar")
    assert e[EXT_PREFIX + "absolute-id"] == model.IRIRef("https://ex.org/ns/foo")
    assert e[EXT_PREFIX + "term-type"] == model.TypedLiteral(
        "x", "https://ex.org/ns/foo"
    )
    assert e[EXT_PREFIX + "prefix-type"] == model.TypedLiteral(
        "x", "https://ex.org/ns/bar"
    )
    assert e[EXT_PREFIX + "non-prefix-type"] == model.TypedLiteral("x", "foo:bar")

    data = model.JSONLDSerializer().serialize_data(objset)
    assert data[EXT_PREFIX + "term-id"] == [{"@id": "foo"}]
    assert data[EXT_PREFIX + "prefix-id"] == [{"@id": "ex:bar"}]
    assert data[EXT_PREFIX + "non-prefix-id"] == [{"@id": "foo:bar"}]
    # Never compacted to the "foo" term
    assert data[EXT_PREFIX + "absolute-id"] == [{"@id": "ex:foo"}]
    assert data[EXT_PREFIX + "term-type"] == [{"@value": "x", "@type": "foo"}]
    assert data[EXT_PREFIX + "prefix-type"] == [{"@value": "x", "@type": "ex:bar"}]
    assert data[EXT_PREFIX + "non-prefix-type"] == [{"@value": "x", "@type": "foo:bar"}]


def test_extensible_json_and_null_values(model, test_context_url, tmp_path):
    DATA = ext_doc(
        test_context_url,
        **{
            EXT_PREFIX
            + "json-prop": {"@value": {"b": 1, "a": [True, None]}, "@type": "@json"},
            EXT_PREFIX + "json-null-prop": {"@value": None, "@type": "@json"},
            EXT_PREFIX + "null-prop": {"@value": None, "@type": XSD + "decimal"},
            EXT_PREFIX
            + "null-list-prop": [
                {"@value": None},
                "a",
                {"@value": None, "@language": "en"},
            ],
        },
    )

    objset, e = ext_value(model, DATA)
    assert e[EXT_PREFIX + "json-prop"] == model.TypedLiteral(
        '{"a":[true,null],"b":1}', RDF_JSON
    )
    assert e[EXT_PREFIX + "json-null-prop"] == model.TypedLiteral("null", RDF_JSON)
    # A null @value is the same as no value
    with pytest.raises(KeyError):
        e[EXT_PREFIX + "null-prop"]
    assert e[EXT_PREFIX + "null-list-prop"] == ["a"]

    expect = {
        EXT_PREFIX
        + "json-prop": [{"@value": {"b": 1, "a": [True, None]}, "@type": "@json"}],
        EXT_PREFIX + "json-null-prop": [{"@value": None, "@type": "@json"}],
        EXT_PREFIX + "null-list-prop": ["a"],
    }

    data = model.JSONLDSerializer().serialize_data(objset)
    for k, v in expect.items():
        assert data[k] == v
    assert EXT_PREFIX + "null-prop" not in data

    inline = strict_json_loads(write_inline(model, objset, tmp_path))["@graph"][0]
    for k, v in expect.items():
        assert inline[k] == v


def test_extensible_value_object_keywords(model, test_context_url):
    DATA = ext_doc(
        test_context_url,
        **{
            EXT_PREFIX + "value-only": {"@value": "a"},
            EXT_PREFIX + "value-index": {"@value": 2, "@index": "idx"},
            EXT_PREFIX
            + "typed-index": {
                "@value": "1.0",
                "@type": XSD + "decimal",
                "@index": "idx",
            },
            EXT_PREFIX + "lang": {"@value": "chat", "@language": "fr"},
            EXT_PREFIX
            + "lang-dir": {
                "@value": "مرحبا",
                "@language": "ar",
                "@direction": "rtl",
            },
        },
    )

    objset, e = ext_value(model, DATA)
    assert e[EXT_PREFIX + "value-only"] == "a"
    assert e[EXT_PREFIX + "value-index"] == 2
    assert e[EXT_PREFIX + "typed-index"] == model.TypedLiteral("1.0", XSD + "decimal")
    assert e[EXT_PREFIX + "lang"] == model.LangString("chat", "fr")
    assert e[EXT_PREFIX + "lang-dir"] == model.LangString("مرحبا", "ar", "rtl")

    data = model.JSONLDSerializer().serialize_data(objset)
    assert data[EXT_PREFIX + "lang"] == [{"@value": "chat", "@language": "fr"}]
    assert data[EXT_PREFIX + "lang-dir"] == [
        {"@value": "مرحبا", "@language": "ar", "@direction": "rtl"}
    ]

    # RDF has no base direction; it is dropped as JSON-LD toRdf does by
    # default
    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    assert g.value(
        rdflib.URIRef(EXT_PREFIX + "e"), rdflib.URIRef(EXT_PREFIX + "lang-dir")
    ) == rdflib.Literal("مرحبا", lang="ar")


def test_typed_literal_lexical_form(model):
    # TypedLiteral holds the lexical form, so equality is RDF term equality
    assert model.TypedLiteral("1.0", XSD + "decimal") != model.TypedLiteral(
        "1.00", XSD + "decimal"
    )
    with pytest.raises(TypeError):
        model.TypedLiteral(1, XSD + "decimal")


def test_encoder_subclass_defaults(model):
    # Encoder subclasses written before value objects existed must still be
    # instantiable, and fall back to the older methods
    calls = []

    class MyEncoder(model.Encoder):
        def write_string(self, v):
            calls.append(("string", v))

        def write_datetime(self, v):
            pass

        def write_integer(self, v):
            pass

        def write_iri(self, v, compact=None):
            calls.append(("iri", v, compact))

        def write_enum(self, v, e, compact=None):
            pass

        def write_bool(self, v):
            pass

        def write_float(self, v):
            calls.append(("float", v))

        def write_object(self, typ, compact_type, id_alias, _id, compact_id, needs_id):
            pass

        def write_property(self, iri, compact=None):
            pass

        def write_list(self):
            pass

        def write_list_item(self):
            pass

        def write_object_list(self):
            pass

        def write_dict(self):
            pass

    enc = MyEncoder()
    enc.write_double(1.5)
    enc.write_iri_ref("http://a/b", "a:b")
    assert calls == [("float", 1.5), ("iri", "http://a/b", "a:b")]

    with pytest.raises(NotImplementedError):
        enc.write_typed_literal("1", XSD + "decimal")
    with pytest.raises(NotImplementedError):
        enc.write_lang_string("a", "en")
    with pytest.raises(NotImplementedError):
        with enc.write_node_object(EXT_PREFIX + "T", None, None, None):
            pass


@pytest.fixture(scope="module")
def alias_model(tmp_path_factory):
    # A model whose context aliases @id and @type, as the SPDX 3 context does
    tmp_directory = tmp_path_factory.mktemp("pythonaliascontext")
    module_name = "pymodel_alias"

    with TEST_CONTEXT.open("r") as f:
        ctx = json.load(f)
    ctx["@context"]["spdxId"] = "@id"
    ctx["@context"]["type"] = "@type"
    context_file = tmp_directory / "alias-context.json"
    with context_file.open("w") as f:
        json.dump(ctx, f)

    shacl2code_generate(
        [
            "--input",
            TEST_MODEL,
            "--context-url",
            context_file,
            ALIAS_CONTEXT_URL,
        ],
        [],
        tmp_directory / module_name,
    )

    sys.path.append(str(tmp_directory))
    try:
        yield importlib.import_module(module_name)
    finally:
        sys.path.remove(str(tmp_directory))
        for mod in list(sys.modules):
            if mod == module_name or mod.startswith(module_name + "."):
                del sys.modules[mod]


ALIAS_CONTEXT_URL = "https://example.org/shacl2code-test/alias-context.json"


def test_extensible_keyword_aliases(alias_model):
    model = alias_model
    DATA = {
        "@context": ALIAS_CONTEXT_URL,
        "type": EXT_PREFIX + "test-extensible",
        "@id": EXT_PREFIX + "e",
        "extensible-class/required": "required",
        EXT_PREFIX + "iri-prop": {"spdxId": EXT_PREFIX + "iri-value"},
        EXT_PREFIX + "literal-prop": {"@value": "0.35", "type": XSD + "decimal"},
    }

    objset = model.SHACLObjectSet()
    model.JSONLDDeserializer().deserialize_data(DATA, objset)
    (e,) = objset.objects
    assert e[EXT_PREFIX + "iri-prop"] == model.IRIRef(EXT_PREFIX + "iri-value")
    assert e[EXT_PREFIX + "literal-prop"] == model.TypedLiteral("0.35", XSD + "decimal")

    data = model.JSONLDSerializer().serialize_data(objset)
    assert data[EXT_PREFIX + "iri-prop"] == [{"@id": EXT_PREFIX + "iri-value"}]
    assert data[EXT_PREFIX + "literal-prop"] == [
        {"@value": "0.35", "@type": XSD + "decimal"}
    ]


def test_custom_objset_index(model, test_context_url):
    # Creates a derived objectset that indexes objects based on a property
    class ObjectSet(model.SHACLObjectSet):
        def create_index(self):
            self.obj_by_string_prop = {}
            super().create_index()

        def add_index(self, obj):
            super().add_index(obj)
            if isinstance(obj, model.test_class):
                self.obj_by_string_prop[obj.test_class_string_scalar_prop] = obj

    objset = ObjectSet()
    d = model.JSONLDDeserializer()
    d.deserialize_data(
        {
            "@context": test_context_url,
            "@graph": [
                {
                    "@type": "test-class",
                    "@id": "https://example.com/test-class-1",
                    "test-class/string-scalar-prop": "first",
                },
                {
                    "@type": "test-class",
                    "@id": "https://example.com/test-class-2",
                    "test-class/string-scalar-prop": "second",
                },
            ],
        },
        objset,
    )

    first = objset.find_by_id("https://example.com/test-class-1")
    assert first

    second = objset.find_by_id("https://example.com/test-class-2")
    assert second

    assert objset.obj_by_string_prop == {
        "first": first,
        "second": second,
    }


def test_metadata(model):
    c = model.test_class()
    c._metadata["foo"] = "bar"
    c._metadata["baz"] = "bat"
    assert c._metadata == {
        "foo": "bar",
        "baz": "bat",
    }

    c._metadata = {
        "foo2": "bar2",
        "baz2": "bat2",
    }

    assert c._metadata == {
        "foo2": "bar2",
        "baz2": "bat2",
    }


def test_object_iter(model):
    o = model.test_class()
    o._id = "http://example.com/link-class"
    o.test_class_string_scalar_prop = "foo"
    o.test_class_string_list_prop = ["a", "b"]
    o.test_class_boolean_prop = True

    data = {k: o[k] for k in o}

    assert data == {
        "@id": "http://example.com/link-class",
        "http://example.org/shacl2code-test/encode": None,
        "http://example.org/shacl2code-test/import": None,
        "http://example.org/shacl2code-test/test-class/anyuri-prop": None,
        "http://example.org/shacl2code-test/test-class/boolean-prop": True,
        "http://example.org/shacl2code-test/test-class/class-list-prop": [],
        "http://example.org/shacl2code-test/test-class/class-prop": None,
        "http://example.org/shacl2code-test/test-class/class-prop-no-class": None,
        "http://example.org/shacl2code-test/test-class/datetime-list-prop": [],
        "http://example.org/shacl2code-test/test-class/datetime-scalar-prop": None,
        "http://example.org/shacl2code-test/test-class/datetimestamp-scalar-prop": None,
        "http://example.org/shacl2code-test/test-class/enum-list-prop": [],
        "http://example.org/shacl2code-test/test-class/enum-prop": None,
        "http://example.org/shacl2code-test/test-class/enum-prop-no-class": None,
        "http://example.org/shacl2code-test/test-class/float-prop": None,
        "http://example.org/shacl2code-test/test-class/integer-prop": None,
        "http://example.org/shacl2code-test/test-class/named-property": None,
        "http://example.org/shacl2code-test/test-class/non-shape": None,
        "http://example.org/shacl2code-test/test-class/nonnegative-integer-prop": None,
        "http://example.org/shacl2code-test/test-class/positive-integer-prop": None,
        "http://example.org/shacl2code-test/test-class/regex": None,
        "http://example.org/shacl2code-test/test-class/regex-datetime": None,
        "http://example.org/shacl2code-test/test-class/regex-datetimestamp": None,
        "http://example.org/shacl2code-test/test-class/regex-list": [],
        "http://example.org/shacl2code-test/test-class/split-string-prop": None,
        "http://example.org/shacl2code-test/test-class/string-list-no-datatype": [],
        "http://example.org/shacl2code-test/test-class/string-list-prop": ["a", "b"],
        "http://example.org/shacl2code-test/test-class/string-scalar-prop": "foo",
    }


def test_extensible_context(model, roundtrip):
    # Test that extensible object IDs and properties account for the context
    objset = model.SHACLObjectSet()
    d = model.JSONLDDeserializer()
    with open(roundtrip, "r") as f:
        d.read(f, objset)

    o = objset.find_by_id("http://serialize.example.com/test-uses-extensible-abstract")
    assert o is not None, "Unable to find object"

    p = o.uses_extensible_abstract_class_prop
    assert p is not None, "Object does not have expected property"

    assert (
        p.get_type() == "http://serialize.example.com/custom-extensible"
    ), "Property does not have expected type"

    assert p["http://custom-prop.example.com/prop"], "Unable to find property value"


def test_object_prop_set_coercion(model):
    """
    Tests that ObjectProp.set() inherently respects and retains both
    raw string IRIs and actual SHACLObject instances securely without
    coercing the object prematurely into a string representation.
    """
    c = model.test_class()

    # Assigning string should remain string
    c.test_class_class_prop = "http://example.org/shacl2code-test/assigned-iri"
    assert isinstance(c.test_class_class_prop, str)
    assert c.test_class_class_prop == "http://example.org/shacl2code-test/assigned-iri"

    # Assigning an object should preserve the object instance without str() coercion
    embedded_obj = model.test_class(
        _id="http://example.org/shacl2code-test/embedded-obj"
    )
    c.test_class_class_prop = embedded_obj
    assert isinstance(c.test_class_class_prop, model.test_class)  # check if same class
    assert c.test_class_class_prop is embedded_obj  # check if same object


def test_introspection(model):
    """
    Tests that defined properties on a class are discoverable
    through Python's introspection mechanisms (e.g., dir()).

    dir() is one of the primary sources for the tab-completion feature in
    Python REPLs and IDEs.
    """
    c = model.test_class()
    props = dir(c)

    # Standard SHACLObject properties
    assert "ID_ALIAS" in props
    assert "NODE_KIND" in props

    # Added properties from test model
    assert "test_class_boolean_prop" in props
    assert "test_class_class_prop" in props
    assert "test_class_integer_prop" in props
    assert "test_class_string_scalar_prop" in props
    assert "test_class_string_list_prop" in props


def test_introspection_extensible(model):
    """
    Tests that defined properties on an extensible class are discoverable
    through Python's introspection mechanisms (e.g., dir()).

    Extensible properties set by IRI are not expected to appear in dir()
    since they are only known at runtime by IRI, not by Python name.
    """
    c = model.extensible_class(extensible_class_required="required")
    props = dir(c)

    # Standard SHACLObject properties
    assert "ID_ALIAS" in props
    assert "NODE_KIND" in props

    # Inherited properties from link_class (extensible_class extends link_class)
    assert "link_class_link_prop" in props
    assert "link_class_link_prop_no_class" in props
    assert "link_class_link_list_prop" in props
    assert "link_class_tag" in props

    # Properties defined on extensible_class itself
    assert "extensible_class_property" in props
    assert "extensible_class_required" in props

    # IRI-keyed extensible properties must NOT appear in dir()
    c["http://example.org/shacl2code-test/extensible-test-prop"] = "test-value"
    assert "http://example.org/shacl2code-test/extensible-test-prop" not in dir(c)


def test_version(model):
    """
    Tests that the version string is correctly mapped.
    """
    from shacl2code.util import convert_version_string

    assert model.VERSION_STRING == MODEL_VERSION
    assert model.VERSION == convert_version_string(MODEL_VERSION)


def test_ontology(model):
    classes = list(model.SHACLObject.CLASSES.values())
    assert classes
    for c in classes:
        assert c.ONTOLOGY is not None


def test_prerelease_warning(model):
    model.SHACL2CODE_TEST.is_prerelease = True

    with pytest.warns(FutureWarning):
        model.test_class()


def test_pre_release_cli_option(tmp_path_factory, test_context_url):
    tmp_directory = tmp_path_factory.mktemp("prerelease_test")
    module_name = "pymodel_prerelease"
    output_dir = tmp_directory / module_name
    shacl2code_generate(
        [
            "--input",
            str(TEST_MODEL),
            "--context",
            test_context_url,
            "--pre-release",
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir,
    )

    sys.path.append(str(tmp_directory))
    try:
        m = importlib.import_module(module_name)
        assert m.SHACL2CODE_TEST.is_prerelease is True
    finally:
        sys.path.remove(str(tmp_directory))
        for mod in list(sys.modules):
            if mod == module_name or mod.startswith(module_name + "."):
                del sys.modules[mod]


def test_no_pre_release_cli_option(tmp_path, test_context_url):
    ttl_content = """
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix sh-to-code: <https://jpewdev.github.io/shacl2code/schema#> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:comment "A test ontology" ;
    rdfs:label "shacl2code-test" ;
    owl:versionInfo "1.0.0" ;
    sh-to-code:isPreRelease true .
"""
    ttl_file = tmp_path / "prerelease.ttl"
    ttl_file.write_text(ttl_content)

    module_name = "pymodel_default_true"
    output_dir = tmp_path / module_name
    shacl2code_generate(
        [
            "--input",
            str(ttl_file),
            "--context",
            test_context_url,
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name)
        assert m.SHACL2CODE_TEST.is_prerelease is True
    finally:
        sys.path.remove(str(tmp_path))

    module_name_no = "pymodel_no_prerelease"
    output_dir_no = tmp_path / module_name_no
    shacl2code_generate(
        [
            "--input",
            str(ttl_file),
            "--context",
            test_context_url,
            "--no-pre-release",
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir_no,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name_no)
        assert m.SHACL2CODE_TEST.is_prerelease is False
    finally:
        sys.path.remove(str(tmp_path))


def test_pre_release_annotations_cases(tmp_path, test_context_url):
    # The number in the comment indicates the precedence of the annotation.
    # 1 is the highest precedence (force by command line option)
    cases = [
        # 2) sh-to-code:isPreRelease
        ("sh-to-code:isPreRelease true .", True),
        ("sh-to-code:isPreRelease false .", False),
        # 3) adms:status (EU SEMIC vocab)
        (
            "adms:status <http://publications.europa.eu/resource/authority/dataset-status/DEVELOP> .",
            True,
        ),
        (
            "adms:status <http://publications.europa.eu/resource/authority/dataset-status/COMPLETED> .",
            False,
        ),
        # 4) adms:status (Original ADMS vocab)
        ("adms:status <http://purl.org/adms/status/UnderDevelopment> .", True),
        ("adms:status <http://purl.org/adms/status/Completed> .", False),
        # 5) bibo:status (Bibliographic Ontology)
        ("bibo:status <http://purl.org/ontology/bibo/status/draft> .", True),
        ("bibo:status <http://purl.org/ontology/bibo/status/published> .", False),
        ("bibo:status <http://purl.org/ontology/bibo/status/legal> .", False),
        # 6) schema:creativeWorkStatus
        ('schema:creativeWorkStatus "Draft" .', True),
        ('schema:creativeWorkStatus "Incomplete" .', True),
        ('schema:creativeWorkStatus "Published" .', False),
        # 7) vs:term_status
        ('vs:term_status "testing" .', True),
        ('vs:term_status "unstable" .', True),
        ('vs:term_status "stable" .', False),
        # 8) owl:versionInfo (pre-release extension)
        ('owl:versionInfo "3.1.0-rc2" .', True),
        ('owl:versionInfo "1.2.1-SNAPSHOT" .', True),
        ('owl:versionInfo "1.0.0.alpha" .', True),
        ('owl:versionInfo "1.0.0" .', False),
        # 9) owl:versionInfo (major version zero)
        ('owl:versionInfo "0.7.1" .', True),
        ('owl:versionInfo "0.0.1" .', True),
        # date-like version must not be mistaken for a semver pre-release
        # suffix (no dotted numeric core precedes the hyphen)
        ('owl:versionInfo "2024-01-15" .', False),
        # Fallback (no annotations or versionInfo at all)
        ('rdfs:comment "A test ontology" .', False),
    ]

    for idx, (annotations, expected) in enumerate(cases):
        ttl_content = f"""
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix sh-to-code: <https://jpewdev.github.io/shacl2code/schema#> .
@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix schema: <http://schema.org/> .
@prefix vs: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .
@prefix bibo: <http://purl.org/ontology/bibo/> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:comment "A test ontology" ;
    rdfs:label "shacl2code-test" ;
    {annotations}
"""
        ttl_file = tmp_path / f"case_{idx}.ttl"
        ttl_file.write_text(ttl_content)

        module_name = f"pymodel_case_{idx}"
        output_dir = tmp_path / module_name
        shacl2code_generate(
            [
                "--input",
                str(ttl_file),
                "--context",
                test_context_url,
            ],
            [
                "--version",
                MODEL_VERSION,
            ],
            output_dir,
        )

        sys.path.append(str(tmp_path))
        try:
            m = importlib.import_module(module_name)
            assert (
                m.SHACL2CODE_TEST.is_prerelease is expected
            ), f"Failed for case {idx}: {annotations}"
        finally:
            sys.path.remove(str(tmp_path))


def test_pre_release_precedence(tmp_path, test_context_url):
    # Example 1:
    # 2) sh-to-code:isPreRelease false (False)
    # 3) adms:status EU SEMIC DEVELOP (True)
    # Expected: False (sh-to-code has higher precedence)
    ttl_content_1 = """
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix sh-to-code: <https://jpewdev.github.io/shacl2code/schema#> .
@prefix adms: <http://www.w3.org/ns/adms#> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:label "shacl2code-test" ;
    sh-to-code:isPreRelease false ;
    adms:status <http://publications.europa.eu/resource/authority/dataset-status/DEVELOP> .
"""
    ttl_file_1 = tmp_path / "prec_1.ttl"
    ttl_file_1.write_text(ttl_content_1)

    module_name_1 = "pymodel_prec_1"
    output_dir_1 = tmp_path / module_name_1
    shacl2code_generate(
        [
            "--input",
            str(ttl_file_1),
            "--context",
            test_context_url,
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir_1,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name_1)
        assert m.SHACL2CODE_TEST.is_prerelease is False
    finally:
        sys.path.remove(str(tmp_path))

    # Example 2:
    # 6) schema:creativeWorkStatus "Published" (False)
    # 7) vs:term_status "testing" (True)
    # Expected: False (creativeWorkStatus has higher precedence)
    ttl_content_2 = """
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix schema: <http://schema.org/> .
@prefix vs: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:label "shacl2code-test" ;
    schema:creativeWorkStatus "Published" ;
    vs:term_status "testing" .
"""
    ttl_file_2 = tmp_path / "prec_2.ttl"
    ttl_file_2.write_text(ttl_content_2)

    module_name_2 = "pymodel_prec_2"
    output_dir_2 = tmp_path / module_name_2
    shacl2code_generate(
        [
            "--input",
            str(ttl_file_2),
            "--context",
            test_context_url,
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir_2,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name_2)
        assert m.SHACL2CODE_TEST.is_prerelease is False
    finally:
        sys.path.remove(str(tmp_path))

    # Example 3:
    # 3) adms:status EU SEMIC DEVELOP (True)
    # 6) schema:creativeWorkStatus "Published" (False)
    # Expected: True (adms:status has higher precedence)
    ttl_content_3 = """
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix schema: <http://schema.org/> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:label "shacl2code-test" ;
    adms:status <http://publications.europa.eu/resource/authority/dataset-status/DEVELOP> ;
    schema:creativeWorkStatus "Published" .
"""
    ttl_file_3 = tmp_path / "prec_3.ttl"
    ttl_file_3.write_text(ttl_content_3)

    module_name_3 = "pymodel_prec_3"
    output_dir_3 = tmp_path / module_name_3
    shacl2code_generate(
        [
            "--input",
            str(ttl_file_3),
            "--context",
            test_context_url,
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir_3,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name_3)
        assert m.SHACL2CODE_TEST.is_prerelease is True
    finally:
        sys.path.remove(str(tmp_path))

    # Example 4:
    # 4) adms:status Original ADMS status Completed (False)
    # 5) bibo:status draft (True)
    # Expected: False (adms:status has higher precedence)
    ttl_content_4 = """
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix bibo: <http://purl.org/ontology/bibo/> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:label "shacl2code-test" ;
    adms:status <http://purl.org/adms/status/Completed> ;
    bibo:status <http://purl.org/ontology/bibo/status/draft> .
"""
    ttl_file_4 = tmp_path / "prec_4.ttl"
    ttl_file_4.write_text(ttl_content_4)

    module_name_4 = "pymodel_prec_4"
    output_dir_4 = tmp_path / module_name_4
    shacl2code_generate(
        [
            "--input",
            str(ttl_file_4),
            "--context",
            test_context_url,
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir_4,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name_4)
        assert m.SHACL2CODE_TEST.is_prerelease is False
    finally:
        sys.path.remove(str(tmp_path))

    # Example 5:
    # 5) bibo:status published (False)
    # 6) schema:creativeWorkStatus Draft (True)
    # Expected: False (bibo:status has higher precedence)
    ttl_content_5 = """
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix schema: <http://schema.org/> .
@prefix bibo: <http://purl.org/ontology/bibo/> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:label "shacl2code-test" ;
    bibo:status <http://purl.org/ontology/bibo/status/published> ;
    schema:creativeWorkStatus "Draft" .
"""
    ttl_file_5 = tmp_path / "prec_5.ttl"
    ttl_file_5.write_text(ttl_content_5)

    module_name_5 = "pymodel_prec_5"
    output_dir_5 = tmp_path / module_name_5
    shacl2code_generate(
        [
            "--input",
            str(ttl_file_5),
            "--context",
            test_context_url,
        ],
        [
            "--version",
            MODEL_VERSION,
        ],
        output_dir_5,
    )

    sys.path.append(str(tmp_path))
    try:
        m = importlib.import_module(module_name_5)
        assert m.SHACL2CODE_TEST.is_prerelease is False
    finally:
        sys.path.remove(str(tmp_path))


def test_pre_release_multi_valued_annotations(tmp_path, test_context_url):
    # Each of these predicates can legally repeat.
    # A stable-looking value listed first must not hide
    # a pre-release-indicating value listed after it.
    cases = [
        # owl:versionInfo: first value stable, second is a semver
        # pre-release extension.
        (
            """
owl:versionInfo "1.0.0" ;
owl:versionInfo "2.0.0-beta" .
""",
            True,
        ),
        # adms:status (EU SEMIC vocab): first value stable, second under
        # development.
        (
            """
adms:status <http://publications.europa.eu/resource/authority/dataset-status/COMPLETED> ;
adms:status <http://publications.europa.eu/resource/authority/dataset-status/DEVELOP> .
""",
            True,
        ),
        # schema:creativeWorkStatus: first value stable, second draft.
        (
            """
schema:creativeWorkStatus "Published" ;
schema:creativeWorkStatus "Draft" .
""",
            True,
        ),
        # vs:term_status: first value stable, second testing.
        (
            """
vs:term_status "stable" ;
vs:term_status "testing" .
""",
            True,
        ),
        # bibo:status: first value published, second draft.
        (
            """
bibo:status <http://purl.org/ontology/bibo/status/published> ;
bibo:status <http://purl.org/ontology/bibo/status/draft> .
""",
            True,
        ),
    ]

    for idx, (annotations, expected) in enumerate(cases):
        ttl_content = f"""
@base <http://example.org/shacl2code-test/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix schema: <http://schema.org/> .
@prefix vs: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .
@prefix bibo: <http://purl.org/ontology/bibo/> .

<http://example.org/shacl2code-test> a owl:Ontology ;
    rdfs:label "shacl2code-test" ;
    {annotations}
"""
        ttl_file = tmp_path / f"multi_{idx}.ttl"
        ttl_file.write_text(ttl_content)

        module_name = f"pymodel_multi_{idx}"
        output_dir = tmp_path / module_name
        shacl2code_generate(
            [
                "--input",
                str(ttl_file),
                "--context",
                test_context_url,
            ],
            [
                "--version",
                MODEL_VERSION,
            ],
            output_dir,
        )

        sys.path.append(str(tmp_path))
        try:
            m = importlib.import_module(module_name)
            assert (
                m.SHACL2CODE_TEST.is_prerelease is expected
            ), f"Failed for case {idx}: {annotations}"
        finally:
            sys.path.remove(str(tmp_path))


def test_custom_type_with_iri_stays_inline(model, test_context_url):
    # An object of a type the model does not define may have no top-level
    # form in the serialization (e.g. an SPDX custom extension), so it must
    # stay inline where it is used, even when it has an IRI
    DATA = {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "uses-extensible-abstract-class",
                "@id": EXT_PREFIX + "user",
                "uses-extensible-abstract-class/prop": {
                    "@type": EXT_PREFIX + "custom-extension",
                    "@id": EXT_PREFIX + "custom",
                    EXT_PREFIX + "p": "v",
                },
            },
            # A second top-level object, so that the serializer writes @graph
            {
                "@type": "uses-extensible-abstract-class",
                "@id": EXT_PREFIX + "other",
                "uses-extensible-abstract-class/prop": {
                    "@type": EXT_PREFIX + "custom-extension",
                },
            },
        ],
    }

    def check(objset):
        doc = model.JSONLDSerializer().serialize_data(objset)
        graph = {o["@id"]: o for o in doc["@graph"]}
        assert sorted(graph) == [EXT_PREFIX + "other", EXT_PREFIX + "user"]
        prop = graph[EXT_PREFIX + "user"]["uses-extensible-abstract-class/prop"]
        assert prop["@id"] == EXT_PREFIX + "custom"
        assert prop[EXT_PREFIX + "p"] == ["v"]

    objset = model.SHACLObjectSet()
    model.JSONLDDeserializer().deserialize_data(DATA, objset)
    check(objset)

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    check(objset2)


def test_custom_type_shared_stays_inline(model, test_context_url):
    # An object of a type the model does not define that is referenced more
    # than once is written inline where it is first used, and referenced by
    # its IRI elsewhere, as it may have no top-level form in the
    # serialization (e.g. an SPDX custom extension)
    DATA = {
        "@context": test_context_url,
        "@graph": [
            {
                "@type": "uses-extensible-abstract-class",
                "@id": EXT_PREFIX + "a-user",
                "uses-extensible-abstract-class/prop": {
                    "@type": EXT_PREFIX + "custom-extension",
                    "@id": EXT_PREFIX + "custom",
                    EXT_PREFIX + "p": ["v"],
                },
            },
            {
                "@type": "uses-extensible-abstract-class",
                "@id": EXT_PREFIX + "b-user",
                "uses-extensible-abstract-class/prop": EXT_PREFIX + "custom",
            },
        ],
    }

    objset = model.SHACLObjectSet()
    model.JSONLDDeserializer().deserialize_data(DATA, objset)
    assert model.JSONLDSerializer().serialize_data(objset) == DATA

    g = rdflib.Graph()
    model.RDFSerializer().write(objset, g)
    objset2 = model.SHACLObjectSet()
    model.RDFDeserializer().read(g, objset2)
    assert model.JSONLDSerializer().serialize_data(objset2) == DATA
