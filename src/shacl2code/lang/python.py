# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""Python language binding renderer"""

import ast
import keyword
import re
from pathlib import Path

from jinja2 import TemplateRuntimeError

from .common import JinjaTemplateRender
from .lang import TEMPLATE_DIR, language
from ..util import convert_version_string

DATATYPE_CLASSES = {
    "http://www.w3.org/2001/XMLSchema#string": "StringProp",
    "http://www.w3.org/2001/XMLSchema#anyURI": "AnyURIProp",
    "http://www.w3.org/2001/XMLSchema#integer": "IntegerProp",
    "http://www.w3.org/2001/XMLSchema#positiveInteger": "PositiveIntegerProp",
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": "NonNegativeIntegerProp",
    "http://www.w3.org/2001/XMLSchema#boolean": "BooleanProp",
    "http://www.w3.org/2001/XMLSchema#decimal": "FloatProp",
    "http://www.w3.org/2001/XMLSchema#dateTime": "DateTimeProp",
    "http://www.w3.org/2001/XMLSchema#dateTimeStamp": "DateTimeStampProp",
}

DATATYPE_PYTHON_TYPES = {
    "http://www.w3.org/2001/XMLSchema#string": "str",
    "http://www.w3.org/2001/XMLSchema#anyURI": "str",
    "http://www.w3.org/2001/XMLSchema#integer": "int",
    "http://www.w3.org/2001/XMLSchema#positiveInteger": "int",
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": "int",
    "http://www.w3.org/2001/XMLSchema#boolean": "bool",
    "http://www.w3.org/2001/XMLSchema#decimal": "float",
    "http://www.w3.org/2001/XMLSchema#dateTime": "datetime",
    "http://www.w3.org/2001/XMLSchema#dateTimeStamp": "datetime",
}


# Names a generated property would collide with; varname() renames it instead.
#
# Class names are not renamed: one landing on a module-level name (e.g.
# "Property", "Optional") fails generation via check_no_shadowed_names().
SHACLOBJECT_RESERVED_WORDS = {
    "AUTO_NAMED_INDIVIDUALS",
    "CLASSES",
    "CLOSED",
    "COMPACT_TYPE",
    "ID_ALIAS",
    "IS_ABSTRACT",
    "IS_DEPRECATED",
    "NAMED_INDIVIDUALS",
    "NODE_KIND",
    "ONTOLOGY",
    "PROPERTIES",
    "TYPE",
    "decode",
    "encode",
    "get_compact_type",
    "get_id",
    "get_type",
    "iter_objects",
    "link_helper",
    "property_keys",
    "set_id",
    "walk",
}


def varname(*name):
    """Make a valid Python variable name."""
    name = "_".join(name)
    # Any invalid characters at the beginning of the name are removed (except "@")
    name = re.sub(r"^[^a-zA-Z0-9_@]*", "", name)
    # Any other invalid characters are replaced with "_" (including "@")
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    # Consolidate runs of "_" to a single one
    name = re.sub(r"__+", "_", name)
    # Append '_' to avoid collisions with Python or SHACLObject keywords
    while keyword.iskeyword(name) or name in SHACLOBJECT_RESERVED_WORDS:
        name = name + "_"
    return name


def prop_element_pytype(prop, classes):
    """Python type of a single element of prop, ignoring container shape.

    Object-reference properties resolve to ``Union[str, 'ClassName']``, since
    they may be set from either an id string or the referenced object.
    """
    if prop.enum_values:
        return "str"
    if prop.class_id:
        return "Union[str, '" + varname(*classes.get(prop.class_id).clsname) + "']"
    return DATATYPE_PYTHON_TYPES[prop.datatype]


def _target_names(target):
    """Names bound by an assignment target, unpacking tuples/lists."""
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, ast.Starred):
        return _target_names(target.value)
    if isinstance(target, (ast.Tuple, ast.List)):
        return [n for t in target.elts for n in _target_names(t)]
    return []


def _is_overload(stmt) -> bool:
    """Whether a def is an @overload stub, which may repeat a name."""
    for dec in stmt.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "overload":
            return True
        if isinstance(dec, ast.Attribute) and dec.attr == "overload":
            return True
    return False


def _scope_bindings(body):
    """Names a statement list binds, as ({name: lineno}, duplicates).

    Mutually exclusive branches (if/else, try/except) are merged rather than
    compared, so a name defined in both arms isn't a redefinition.
    """
    names: dict = {}
    dups: list = []

    def add(name, lineno):
        if name in names:
            dups.append((name, names[name], lineno))
        else:
            names[name] = lineno

    def branches(*bodies):
        merged: dict = {}
        for b in bodies:
            sub_names, sub_dups = _scope_bindings(b)
            dups.extend(sub_dups)
            for n, lineno in sub_names.items():
                merged.setdefault(n, lineno)
        for n, lineno in merged.items():
            add(n, lineno)

    for stmt in body:
        if isinstance(stmt, ast.Import):
            for a in stmt.names:
                add(a.asname or a.name.split(".")[0], stmt.lineno)
        elif isinstance(stmt, ast.ImportFrom):
            for a in stmt.names:
                if a.name != "*":
                    add(a.asname or a.name, stmt.lineno)
        elif isinstance(stmt, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not _is_overload(stmt):
                add(stmt.name, stmt.lineno)
        elif isinstance(stmt, ast.Assign):
            for t in stmt.targets:
                for n in _target_names(t):
                    add(n, stmt.lineno)
        elif isinstance(stmt, ast.AnnAssign):
            for n in _target_names(stmt.target):
                add(n, stmt.lineno)
        elif isinstance(stmt, ast.If):
            branches(stmt.body, stmt.orelse)
        elif isinstance(stmt, ast.Try):
            branches(
                stmt.body,
                *[h.body for h in stmt.handlers],
                stmt.orelse,
                stmt.finalbody,
            )
        elif isinstance(stmt, (ast.For, ast.While, ast.With)):
            branches(stmt.body)

    return names, dups


def check_no_shadowed_names(text: str, filename: str) -> None:
    """Reject generated Python that binds one top-level name twice.

    A model-derived class or constant landing on a name the module already
    imports silently rebinds it -- a class named "Optional", for instance,
    replaces typing.Optional for every annotation after it. Parsing the
    rendered output catches every such collision for every generated module,
    with no per-module reserved-word list to maintain.
    """
    try:
        tree = ast.parse(text, filename=filename)
    except SyntaxError as e:
        raise TemplateRuntimeError(
            f"{filename}: generated invalid Python: {e}"
        ) from None

    _, dups = _scope_bindings(tree.body)
    if dups:
        detail = "; ".join(
            f"{n!r} (line {first}, again on line {second})"
            for n, first, second in sorted(dups)
        )
        raise TemplateRuntimeError(
            f"{filename}: generated code binds the same top-level name twice: "
            f"{detail}. A model name most likely collides with an import or "
            "another class; rename it in the model or context."
        )


@language("python")
class PythonRender(JinjaTemplateRender):
    """Render Python Language Bindings."""

    HELP = "Python Language Bindings"

    FILES = (
        "__init__.py",
        "model.py",
        "model.pyi",
    )

    def __init__(self, args):
        super().__init__(args)
        self.__output = args.output
        self.__use_slots = args.use_slots
        self.__include_main = args.include_main == "yes"
        self.__version_str = args.version
        if args.version:
            self.__version = repr(convert_version_string(args.version))
        else:
            self.__version = ""

    @classmethod
    def get_arguments(cls, parser):
        parser.add_argument(
            "--output",
            "-o",
            type=Path,
            help="Output directory",
            required=True,
        )
        parser.add_argument(
            "--include-main",
            choices=("yes", "no"),
            default="yes",
            help="Generate a main function for the module. Default is '%(default)s'",
        )
        parser.add_argument(
            "--use-slots",
            choices=("auto", "yes", "no"),
            default="auto",
            help=(
                "Use __slot__ to reduce memory usage. "
                "Slots prevents multiple inheritance. Default is %(default)s"
            ),
        )
        parser.add_argument(
            "--version",
            help="Specify model version",
        )

    def get_outputs(self):
        t = TEMPLATE_DIR / "python"
        self.__output.mkdir(parents=True, exist_ok=True)

        def get_file(name):
            return self.__output / name, t / (name + ".j2"), {}

        for s in self.FILES:
            yield get_file(s)

        if self.__include_main:
            yield get_file("cmd.py")
            yield get_file("cmd.pyi")
            yield get_file("__main__.py")

    def get_extra_env(self):
        return {
            "varname": varname,
            "prop_element_pytype": prop_element_pytype,
            "DATATYPE_CLASSES": DATATYPE_CLASSES,
            "DATATYPE_PYTHON_TYPES": DATATYPE_PYTHON_TYPES,
        }

    def validate_render(self, text, name):
        # Backstop for every generated module: a model name landing on a
        # name the module already binds would otherwise silently shadow it.
        if name.endswith((".py.j2", ".pyi.j2")):
            check_no_shadowed_names(text, name[: -len(".j2")])

    def get_additional_render_args(self, model):
        if self.__use_slots == "auto":
            use_slots = all(len(cls.parent_ids) <= 1 for cls in model.classes)
        elif self.__use_slots == "yes":
            use_slots = True
        else:
            use_slots = False
        return {
            "use_slots": use_slots,
            "include_main": self.__include_main,
            "version_str": self.__version_str,
            "version": self.__version,
        }
