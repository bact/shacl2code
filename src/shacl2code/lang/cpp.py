#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""C++ language binding renderer"""

import re
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Tuple

from ..version import VERSION
from .common import JinjaTemplateRender
from .lang import TEMPLATE_DIR, language

if TYPE_CHECKING:
    import argparse

    from ..model import Class, Model, Property


def varname(*name: str) -> str:
    """Convert names to a valid C++ identifier."""
    joined = "_".join(name)
    # Any invalid characters at the beginning of the name are removed (except
    # "@")
    joined = re.sub(r"^[^a-zA-Z0-9_@]*", "", joined)
    # Any other invalid characters are replaced with "_" (including "@")
    joined = re.sub(r"[^a-zA-Z0-9_]", "_", joined)
    # Consolidate runs of "_" to a single one
    joined = re.sub(r"__+", "_", joined)
    return joined


def parent_cpp_classes(cls: "Class", classes: Any) -> List[str]:
    """Return the C++ parent class name list for a class."""
    if cls.parent_ids:
        parents = [varname(*classes.get(i).clsname) for i in cls.parent_ids]
    else:
        parents = ["SHACLObject"]

    if cls.is_extensible:
        parents = [f"SHACLExtensibleObject<{p}>" for p in parents]

    return parents


def prop_is_list(prop: "Property") -> bool:
    """Return True if the property is a list (max_count != 1)."""
    return prop.max_count is None or prop.max_count != 1


def id_str(s: str) -> str:
    """Replace non-alphanumeric characters with underscores."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", s)


def comment_wrap(s: str) -> str:
    """Wrap a string in C++ comment markers."""
    return "\n".join(["*/", s, "/*"])


@language("cpp")
class CppRender(JinjaTemplateRender):
    """Render C++ Language Bindings."""

    HELP = "C++ Language Bindings"

    SOURCES = (
        "datetime.cpp",
        "decode.cpp",
        "encode.cpp",
        "errorhandler.cpp",
        "extensible.cpp",
        "link.cpp",
        "namedindividual.cpp",
        "object.cpp",
        "objectpath.cpp",
        "objectset.cpp",
        "property.cpp",
        "propertyvalue.cpp",
        "refproperty.cpp",
        "type.cpp",
        "util.cpp",
    )

    HEADERS = (
        "api.hpp",
        "datetime.hpp",
        "decode.hpp",
        "encode.hpp",
        "errorhandler.hpp",
        "exceptions.hpp",
        "extensible.hpp",
        "link.hpp",
        "namedindividual.hpp",
        "object.hpp",
        "objectpath.hpp",
        "objectset.hpp",
        "prop.hpp",
        "property.hpp",
        "propertyvalue.hpp",
        "ref.hpp",
        "refproperty.hpp",
        "type.hpp",
        "util.hpp",
        "walk.hpp",
    )

    def __init__(self, args: Any) -> None:
        super().__init__(args)
        self.basename: Path = args.basename
        self.namespace: str = args.namespace or id_str(args.basename.name)
        self.lib_version: str = args.version
        self.description: str = (
            args.description or f"shacl2code generated binding {args.basename.name}"
        )
        self.macro_prefix: str = id_str("SHACL2CODE_" + self.basename.name).upper()

    @classmethod
    def get_arguments(cls, parser: "argparse.ArgumentParser") -> None:
        parser.add_argument(
            "--output",
            "-o",
            type=Path,
            help="Output file basename",
            dest="basename",
            required=True,
        )

        parser.add_argument(
            "--namespace",
            "-n",
            help="Output namespace. If unspecified, defaults to output basename",
        )

        parser.add_argument(
            "--version",
            metavar="MAJOR[.MINOR[.MICRO]]",
            default=VERSION,
            help="Library version",
        )

        parser.add_argument(
            "--description",
            help="Library description",
        )

    def get_outputs(self) -> Iterator[Tuple[Path, Path, Dict[str, Any]]]:
        def suffix(s: str) -> Path:
            return self.basename.parent / (self.basename.name + s)

        t = TEMPLATE_DIR / "cpp"

        for s in self.SOURCES:
            yield self.basename.parent / s, t / (s + ".j2"), {}

        for s in self.HEADERS:
            guard = f"_{self.macro_prefix}_{id_str(s).upper()}"
            yield self.basename.parent / s, t / (s + ".j2"), {
                "guard_begin": comment_wrap(textwrap.dedent(f"""\
                        #ifndef {guard}
                        #define {guard}
                        """)),
                "guard_end": comment_wrap(f"#endif // {guard}"),
            }

        yield suffix(".cpp"), t / "source.j2", {}
        yield suffix(".hpp"), t / "header.j2", {
            "headers": self.HEADERS,
        }
        yield suffix("-jsonld.cpp"), t / "jsonld-source.j2", {}
        yield suffix("-jsonld.hpp"), t / "jsonld-header.j2", {}

        yield self.basename.parent / "Makefile", t / "Makefile.j2", {
            "lib_obj_files": " ".join(
                s.replace(".cpp", ".o")
                for s in self.SOURCES
                + (
                    f"{self.basename.name}.cpp",
                    f"{self.basename.name}-jsonld.cpp",
                )
            ),
            "headers": self.HEADERS
            + (
                f"{self.basename.name}.hpp",
                f"{self.basename.name}-jsonld.hpp",
            ),
        }

        yield suffix("-validate.cpp"), t / "validate.j2", {}
        yield suffix(".pc"), t / "pkgconfig.pc.j2", {}
        yield self.basename.parent / "Doxyfile", t / "Doxyfile.j2", {}

    def get_extra_env(self) -> Dict[str, Any]:
        return {
            "varname": varname,
            "prop_is_list": prop_is_list,
            "parent_cpp_classes": parent_cpp_classes,
            "macro_prefix": self.macro_prefix,
            "api_def_begin": comment_wrap(textwrap.dedent(f"""\
                    #ifndef DOXYGEN_SKIP
                    #include "api.hpp"
                    // These are so that we don't have to use Jinja templates below since that messes up the formatting
                    #define EXPORT {self.macro_prefix}_API
                    #define LOCAL  {self.macro_prefix}_LOCAL
                    #endif // DOXYGEN_SKIP
                    """)),
            "api_def_end": comment_wrap(textwrap.dedent("""\
                    #undef EXPORT
                    #undef LOCAL
                    """)),
            "ns_begin": comment_wrap(
                "\n".join(f"namespace {n} {{" for n in self.namespace.split("::"))
            ),
            "ns_end": comment_wrap("\n".join("}" for n in self.namespace.split("::"))),
        }

    def get_additional_render_args(self, model: "Model") -> Dict[str, Any]:
        return {
            "basename": self.basename.name,
            "namespace": self.namespace,
            "nsprefix": f"::{self.namespace}" if self.namespace else "",
            "lib_version": self.lib_version,
            "lib_description": self.description,
        }
