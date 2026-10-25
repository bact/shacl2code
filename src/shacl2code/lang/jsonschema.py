#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""JSON Schema renderer"""

import keyword
import re

from .common import BasicJinjaRender
from .lang import TEMPLATE_DIR, language


def varname(*name):
    name = str("_".join(name)).replace("@", "_")
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    while keyword.iskeyword(name):
        name = name + "_"
    return name


def context_reserved_names(model):
    """
    Returns the names an additional context object must not define, sorted

    These are all the names defined at the top level of the model contexts:
    terms, prefixes and keyword aliases, plus any keyword the model contexts
    set (e.g. "@base" or "@vocab"). Redefining any of them in a later context
    would change how the model's terms or IRIs expand.

    They also include the short names the schema accepts for model IRIs: class
    and property names, enumeration values and named individuals. A JSON-LD
    processor tries terms before "@vocab", so a new term with one of these
    names would change what the name expands to even when no model context
    defines it as a term (e.g. an enumeration value that only expands through
    the "@vocab" of a property-scoped context). Compact IRIs and absolute IRIs
    are skipped: their prefix is already reserved, or they are not terms.
    """
    context = model.context
    names = set()
    for ctx in context.contexts:
        if isinstance(ctx, dict):
            ctx = [ctx]
        for c in ctx:
            if isinstance(c, dict):
                names |= set(c.keys())

    short = set()
    for cls in model.classes:
        short.add(context.compact_vocab(cls._id))
        for n in cls.named_individuals or []:
            short.add(context.compact_iri(n._id))
        for prop in cls.properties:
            short.add(context.compact_vocab(prop.path))
            for e in prop.enum_values or []:
                short.add(context.compact_vocab(e, prop.path))
    names |= {n for n in short if ":" not in n}
    return sorted(names)


@language("jsonschema")
class JsonSchemaRender(BasicJinjaRender):
    HELP = "JSON Schema"

    def __init__(self, args):
        super().__init__(args, TEMPLATE_DIR / "jsonschema.j2")
        self.__render_args = {
            "schema_title": args.title,
            "schema_id": args.id,
            "allow_elided_lists": args.allow_elided_lists,
        }

    @classmethod
    def get_arguments(cls, parser):
        super().get_arguments(parser)

        parser.add_argument("--title", help="Schema title")
        parser.add_argument("--id", help="Schema ID")
        parser.add_argument(
            "--allow-elided-lists",
            action="store_true",
            help="Allow lists to be elided if they only contain a single element",
        )

    def get_extra_env(self):
        return {
            "varname": varname,
        }

    def get_additional_render_args(self, model):
        return {
            **self.__render_args,
            "context_reserved_names": context_reserved_names(model),
        }
