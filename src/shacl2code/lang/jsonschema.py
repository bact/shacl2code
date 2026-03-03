#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""JSON Schema renderer"""

import keyword
import re
from typing import TYPE_CHECKING, Any, Dict

from .common import BasicJinjaRender
from .lang import TEMPLATE_DIR, language

if TYPE_CHECKING:
    import argparse

    from ..model import Model


def varname(*name: str) -> str:
    """Convert names to a valid JSON Schema identifier."""
    joined = str("_".join(name)).replace("@", "_")
    joined = re.sub(r"[^a-zA-Z0-9_]", "", joined)
    while keyword.iskeyword(joined):
        joined = joined + "_"
    return joined


@language("jsonschema")
class JsonSchemaRender(BasicJinjaRender):
    """Render JSON Schema output."""

    HELP = "JSON Schema"

    def __init__(self, args: Any) -> None:
        super().__init__(args, TEMPLATE_DIR / "jsonschema.j2")
        self.__render_args: Dict[str, Any] = {
            "schema_title": args.title,
            "schema_id": args.id,
            "allow_elided_lists": args.allow_elided_lists,
        }

    @classmethod
    def get_arguments(cls, parser: "argparse.ArgumentParser") -> None:
        super().get_arguments(parser)

        parser.add_argument("--title", help="Schema title")
        parser.add_argument("--id", help="Schema ID")
        parser.add_argument(
            "--allow-elided-lists",
            action="store_true",
            help="Allow lists to be elided if they only contain a single element",
        )

    def get_extra_env(self) -> Dict[str, Any]:
        return {
            "varname": varname,
        }

    def get_additional_render_args(self, model: "Model") -> Dict[str, Any]:
        return self.__render_args
