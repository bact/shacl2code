# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""Python language binding renderer"""

import keyword
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterator, Tuple

from .common import JinjaTemplateRender
from .lang import TEMPLATE_DIR, language

if TYPE_CHECKING:
    import argparse

    from ..model import Model

DATATYPE_CLASSES: Dict[str, str] = {
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

DATATYPE_PYTHON_TYPES: Dict[str, str] = {
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


def varname(*name: str) -> str:
    """Make a valid Python variable name."""
    joined = "_".join(name)
    # Any invalid characters at the beginning of the name are removed (except "@")
    joined = re.sub(r"^[^a-zA-Z0-9_@]*", "", joined)
    # Any other invalid characters are replaced with "_" (including "@")
    joined = re.sub(r"[^a-zA-Z0-9_]", "_", joined)
    # Consolidate runs of "_" to a single one
    joined = re.sub(r"__+", "_", joined)
    # Add a _ to anything that is a python keyword
    while keyword.iskeyword(joined):
        joined = joined + "_"
    return joined


@language("python")
class PythonRender(JinjaTemplateRender):
    """Render Python Language Bindings."""

    HELP = "Python Language Bindings"

    FILES = (
        "main.py",
        "stub.pyi",
    )

    def __init__(self, args: Any) -> None:
        super().__init__(args)
        self.__output: Path = args.output
        self.__use_slots: str = args.use_slots
        self.__render_args: Dict[str, Any] = {
            "elide_lists": args.elide_lists,
        }

    @classmethod
    def get_arguments(cls, parser: "argparse.ArgumentParser") -> None:
        parser.add_argument(
            "--output",
            "-o",
            type=Path,
            help="Output directory",
            required=True,
        )
        parser.add_argument(
            "--elide-lists",
            action="store_true",
            help="Elide lists when writing documents if they only contain a single item",
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

    def get_outputs(self) -> Iterator[Tuple[Path, Path, Dict[str, Any]]]:
        t = TEMPLATE_DIR / "python"
        self.__output.mkdir(parents=True, exist_ok=True)

        for s in self.FILES:
            yield self.__output / s, t / (s + ".j2"), {}

    def get_extra_env(self) -> Dict[str, Any]:
        return {
            "varname": varname,
            "DATATYPE_CLASSES": DATATYPE_CLASSES,
            "DATATYPE_PYTHON_TYPES": DATATYPE_PYTHON_TYPES,
        }

    def get_additional_render_args(self, model: "Model") -> Dict[str, Any]:
        if self.__use_slots == "auto":
            use_slots = all(len(cls.parent_ids) <= 1 for cls in model.classes)
        elif self.__use_slots == "yes":
            use_slots = True
        else:
            use_slots = False
        return {
            "use_slots": use_slots,
            **self.__render_args,
        }
