# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""Python language binding renderer"""

import ast
import builtins
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


def get_all_parent_ids(cls, classes):
    """Get all ancestor class IDs."""
    result = set()
    for pid in cls.parent_ids:
        result.add(pid)
        parent = classes.get(pid)
        result |= get_all_parent_ids(parent, classes)
    return result


def is_effectively_extensible(cls, classes):
    """Check if a class or any of its ancestors is extensible.

    The runtime __init__ is always inherited (classes never define their
    own), so a subclass of an extensible class accepts ``typ`` even when its
    own ``is_extensible`` flag is unset.
    """
    if cls.is_extensible:
        return True
    for pid in get_all_parent_ids(cls, classes):
        if classes.get(pid).is_extensible:
            return True
    return False


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


# Non-dunder names the interpreter falls back to when a module doesn't bind
# them itself -- a module-level rebinding of one it also uses is a real bug.
_BUILTIN_NAMES = frozenset(n for n in dir(builtins) if not n.startswith("_"))


def _used_builtins(tree):
    """Builtin names the module loads anywhere (even inside a function
    body), so a later module-level rebinding of one is checked as a dup."""
    return {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and node.id in _BUILTIN_NAMES
    }


# Statement kinds with their own scope: a walrus in their BODY doesn't bind
# at module scope. Their other fields (decorators, argument defaults/
# annotations, class bases/keywords) still run at module scope when the
# def/class statement executes, so those are walked, not skipped.
_WALRUS_SCOPE_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


def _reject_module_walrus(tree, filename):
    """Raise if a walrus assignment appears anywhere at module scope.

    A comprehension/generator expression is NOT a scope boundary here: PEP
    572 binds its walrus target in the nearest enclosing non-comprehension
    scope, which -- since a function/lambda/class body stops this walk --
    is always module scope by the time this walk reaches one.

    _scope_bindings doesn't model the binding a walrus introduces, so this
    runs once upfront rather than checking each statement kind separately.
    """
    where = filename or "<generated>"

    def walk(node):
        for name, value in ast.iter_fields(node):
            if isinstance(node, _WALRUS_SCOPE_DEFS) and name == "body":
                continue
            for child in value if isinstance(value, list) else [value]:
                if not isinstance(child, ast.AST):
                    continue
                if isinstance(child, ast.NamedExpr):
                    raise TemplateRuntimeError(
                        f"{where}: name-collision check does not understand "
                        f"module-level NamedExpr at line {child.lineno} "
                        "(walrus assignment); extend _scope_bindings"
                    )
                walk(child)

    walk(tree)


def _scope_bindings(
    body, filename=None, prebound=None, star_names=None, package_init=False
):
    """Names a statement list binds, as ({name: lineno}, duplicates).

    Only understands the module-level statement kinds the Python templates
    actually emit: imports, class/function defs, (ann/aug)assignments, a
    bare expression statement, pass, if, and a try restricted to a plain
    body/except/else (no ``finally``, no ``except ... as name``). Anything
    else -- e.g. a `global` statement or a `for`/`while`/`with`/`match` --
    raises, rather than silently missing a binding it doesn't model. (A
    module-level walrus is rejected upfront by _reject_module_walrus,
    before this is called.)

    Mutually exclusive branches (if/else, try/except) are merged rather than
    compared, so a name defined in both arms isn't a redefinition. A try's
    body and orelse run as one sequential path, and each handler is an
    alternative to that path.

    A name bound by ``from __future__ import ...`` is not tracked: it's a
    compiler directive consumed before the module runs (e.g. `annotations`
    is briefly bound to a `_Feature` object), so a class reusing that name
    later harmlessly replaces a value nothing else in the module reads.

    star_names maps a relative import's module name (as in ``from .foo
    import *``, always level 1) to the names it exports; always
    fail-closed, raising if the target isn't a key in star_names (which
    itself may be None).

    package_init is True when checking a package's own __init__.py, where a
    module-level ``def __getattr__`` raises (lazy attribute access isn't
    modeled) and prebound is expected to include the package's sibling
    module names (see check_no_shadowed_names).

    prebound seeds the returned scope with pre-existing bindings, keyed by
    a sentinel lineno (0: a used builtin; -1: a sibling package module) that
    describe() in check_no_shadowed_names turns into a clearer message; only
    meaningful on the outermost call, since nested calls merge into the
    caller's scope.
    """
    names: dict = dict(prebound) if prebound else {}
    dups: list = []

    def add(name, lineno):
        if name in names:
            dups.append((name, names[name], lineno))
        else:
            names[name] = lineno

    def branches(*bodies):
        merged: dict = {}
        for b in bodies:
            sub_names, sub_dups = _scope_bindings(
                b, filename, star_names=star_names, package_init=package_init
            )
            dups.extend(sub_dups)
            for n, lineno in sub_names.items():
                merged.setdefault(n, lineno)
        for n, lineno in merged.items():
            add(n, lineno)

    def unsupported(stmt, detail=None):
        where = filename or "<generated>"
        msg = (
            f"{where}: name-collision check does not understand module-level "
            f"{type(stmt).__name__} at line {stmt.lineno}"
        )
        if detail:
            msg += f" ({detail})"
        raise TemplateRuntimeError(msg + "; extend _scope_bindings")

    for stmt in body:
        if isinstance(stmt, ast.Import):
            for a in stmt.names:
                add(a.asname or a.name.split(".")[0], stmt.lineno)
        elif isinstance(stmt, ast.ImportFrom):
            if stmt.module == "__future__":
                continue
            for a in stmt.names:
                if a.name == "*":
                    exported = (
                        (star_names or {}).get(stmt.module) if stmt.level == 1 else None
                    )
                    if exported is None:
                        where = filename or "<generated>"
                        raise TemplateRuntimeError(
                            f"{where}: line {stmt.lineno}: `from "
                            f"{'.' * stmt.level}{stmt.module or ''} import *` "
                            "cannot be checked -- target module's exports "
                            "are unknown"
                        )
                    for n in exported:
                        add(n, stmt.lineno)
                else:
                    add(a.asname or a.name, stmt.lineno)
        elif isinstance(stmt, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if (
                package_init
                and isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))
                and stmt.name == "__getattr__"
            ):
                where = filename or "<generated>"
                raise TemplateRuntimeError(
                    f"{where}: line {stmt.lineno}: lazy __getattr__ in "
                    "__init__ is not supported by the collision check yet"
                )
            if not _is_overload(stmt):
                add(stmt.name, stmt.lineno)
        elif isinstance(stmt, ast.Assign):
            for t in stmt.targets:
                for n in _target_names(t):
                    add(n, stmt.lineno)
        elif isinstance(stmt, ast.AnnAssign):
            for n in _target_names(stmt.target):
                add(n, stmt.lineno)
        elif isinstance(stmt, (ast.AugAssign, ast.Expr, ast.Pass)):
            pass  # AugAssign augments an existing name; binds nothing new.
        elif isinstance(stmt, ast.If):
            branches(stmt.body, stmt.orelse)
        elif isinstance(stmt, ast.Try):
            if stmt.finalbody:
                unsupported(stmt, "try/finally")
            if any(h.name is not None for h in stmt.handlers):
                unsupported(stmt, "except ... as name")
            branches(stmt.body + stmt.orelse, *[h.body for h in stmt.handlers])
        else:
            unsupported(stmt)

    return names, dups


def _extract_all(text: str, filename: str):
    """Names a module exports via ``__all__ = [...]`` / ``__all__ += [...]``
    at module level or in the body of a module-level try. Fail-closed: if
    __all__ is touched anywhere else this scan doesn't collect (e.g. inside
    an ``if`` or a class body), or assigned a non-literal or a non-string
    entry, raises. None if __all__ is never assigned.
    """
    tree = ast.parse(text, filename=filename)
    names = None
    collected = 0

    def collect(node):
        nonlocal names, collected
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, op = node.targets[0], "="
        elif isinstance(node, ast.AugAssign):
            target, op = node.target, "+="
        else:
            return
        if not (isinstance(target, ast.Name) and target.id == "__all__"):
            return

        valid = isinstance(node.value, (ast.List, ast.Tuple)) and all(
            isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            for elt in node.value.elts
        )
        if not valid:
            raise TemplateRuntimeError(
                f"{filename}: line {node.lineno}: __all__ {op} ... must be "
                "a literal list/tuple of strings"
            )

        entries = [elt.value for elt in node.value.elts]
        names = entries if op == "=" else (names or []) + entries
        collected += 1

    for node in tree.body:
        collect(node)
        if isinstance(node, ast.Try):
            for sub in node.body:
                collect(sub)

    total = sum(
        1
        for n in ast.walk(tree)
        if isinstance(n, ast.Name)
        and n.id == "__all__"
        and isinstance(n.ctx, ast.Store)
    )
    if total != collected:
        raise TemplateRuntimeError(f"{filename}: unsupported __all__ construction")

    return names


def check_no_shadowed_names(
    text: str,
    filename: str,
    star_names=None,
    package_init=False,
    class_iris=None,
    submodules=None,
) -> None:
    """Reject generated Python that binds one top-level name twice.

    A model-derived class or constant landing on a name the module already
    imports, or a builtin it uses, silently rebinds it -- a class named
    "Optional" or "str", for instance, replaces that name for every use
    after it, including inside function bodies defined earlier.

    star_names and package_init are as in _scope_bindings. submodules, used
    only when package_init, is the package's sibling module base names
    (e.g. {"model", "cmd"}): Python sets each as an attribute of the
    package on import regardless of whether __init__.py itself imports it,
    so all of them are prebound rather than only ones __init__.py imports.
    class_iris, if given, maps a Python name to the source class IRI(s) it
    was generated from, to name in the error.
    """
    try:
        tree = ast.parse(text, filename=filename)
    except SyntaxError as e:
        raise TemplateRuntimeError(
            f"{filename}: generated invalid Python: {e}"
        ) from None

    _reject_module_walrus(tree, filename)

    prebound = {n: 0 for n in _used_builtins(tree)}
    if package_init:
        for n in submodules or ():
            prebound.setdefault(n, -1)

    _, dups = _scope_bindings(
        tree.body,
        filename,
        prebound=prebound,
        star_names=star_names,
        package_init=package_init,
    )
    if dups:

        def describe(n, first, second):
            if first == 0:
                loc = (
                    f"{n!r} shadows a builtin used by the generated code "
                    f"(line {second})"
                )
            elif first == -1:
                loc = (
                    f"{n!r} shadows this package's own {n!r} submodule, "
                    f"which Python binds as a package attribute on import "
                    f"(line {second})"
                )
            else:
                loc = f"{n!r} (line {first}, again on line {second})"
            iris = class_iris.get(n) if class_iris else None
            if iris:
                loc += f" [class: {', '.join(iris)}]"
            return loc

        detail = "; ".join(
            describe(n, first, second) for n, first, second in sorted(dups)
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

    # model.py/model.pyi must render before __init__.py: validate_render
    # records their __all__ to expand __init__.py's `from .model import *`.
    FILES = (
        "model.py",
        "model.pyi",
        "__init__.py",
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
        # module stem ("model") -> names in its rendered __all__, for
        # expanding star-imports; populated as each .py file is validated.
        self.__module_all = {}
        self.__class_iris = {}
        # Sibling module base names this renderer emits (all of FILES but
        # __init__.py itself, plus cmd/__main__ when include-main): Python
        # binds each as a package attribute on import, whether or not
        # __init__.py itself imports it.
        self.__submodules = {Path(f).stem for f in self.FILES if f != "__init__.py"}
        if self.__include_main:
            self.__submodules |= {"cmd", "__main__"}

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
            "is_effectively_extensible": is_effectively_extensible,
            "DATATYPE_CLASSES": DATATYPE_CLASSES,
            "DATATYPE_PYTHON_TYPES": DATATYPE_PYTHON_TYPES,
        }

    def validate_render(self, text, name):
        # Backstop for every generated module: a model name landing on a
        # name the module already binds would otherwise silently shadow it.
        if not name.endswith((".py.j2", ".pyi.j2")):
            return

        filename = name[: -len(".j2")]
        check_no_shadowed_names(
            text,
            filename,
            star_names=self.__module_all,
            package_init=(name == "__init__.py.j2"),
            class_iris=self.__class_iris,
            submodules=self.__submodules,
        )

        # Record model.py's __all__ so a later `from .model import *`
        # (in __init__.py) can be expanded and checked too.
        if name.endswith(".py.j2"):
            stem = filename[: -len(".py")]
            self.__module_all[stem] = _extract_all(text, filename)

    def get_additional_render_args(self, model):
        self.__module_all = {}
        self.__class_iris = {}
        for cls in model.classes:
            self.__class_iris.setdefault(varname(*cls.clsname), []).append(cls._id)

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
