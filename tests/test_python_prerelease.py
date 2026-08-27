# SPDX-FileCopyrightText: 2024 Joshua Watt
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT

import importlib
import sys
from pathlib import Path

import pytest

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent

DATA_DIR = THIS_DIR / "data"

TEST_MODEL = THIS_DIR / "data" / "model" / "test.ttl"

MODEL_VERSION = "1.0.0.alpha"


def shacl2code_generate(args, python_args, outfile):
    import subprocess

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
