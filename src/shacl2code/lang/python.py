#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT

from .common import BasicJinjaRender, OutputFile
from .lang import language, TEMPLATE_DIR

import re
import keyword


def varname(*name):
    name = "_".join(name)
    # Any invalid characters at the beginning of the name are removed (except
    # "@")
    name = re.sub(r"^[^a-zA-Z0-9_@]*", "", name)
    # Any other invalid characters are replaced with "_" (including "@")
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    # Consolidate runs of "_" to a single one
    name = re.sub(r"__+", "_", name)
    # Add a _ to anything that is a python keyword
    while keyword.iskeyword(name):
        name = name + "_"
    return name


@language("python")
class PythonRender(BasicJinjaRender):
    HELP = "Python Language Bindings"

    def __init__(self, args):
        super().__init__(args, TEMPLATE_DIR / "python.j2")
        self.__use_slots = args.use_slots
        self.__render_args = {
            "elide_lists": args.elide_lists,
        }

    @classmethod
    def get_arguments(cls, parser):
        super().get_arguments(parser)

        parser.add_argument(
            "--elide-lists",
            action="store_true",
            help="Elide lists when writing documents if they only contain a single item",
        )
        parser.add_argument(
            "--use-slots",
            choices=("auto", "yes", "no"),
            default="auto",
            help="Use __slot__ to reduce memory usage. Slots prevents multiple inheritance. Default is %(default)s",
        )

    def get_extra_env(self):
        return {
            "varname": varname,
        }

    def get_additional_render_args(self, model):
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

    def get_outputs(self):
        """
        Emit both the runtime `.py` and the type stub `.pyi` alongside it.

        Behavior:
        - If output is `-` (stdout), only the `.py` is written to stdout.
        - If output is a file path, write `<path>` with the runtime template and
          `<path-with-.pyi-suffix>` with the stub template.
        """
        template_py = TEMPLATE_DIR / "python.py.j2"
        template_pyi = TEMPLATE_DIR / "python.pyi.j2"

        out = getattr(self, "_BasicJinjaRender__output", None)
        if out is None:
            # Fallback to default behavior
            yield self._BasicJinjaRender__output, self._BasicJinjaRender__template, {}
            return

        # If output is stdout, only emit the runtime .py to stdout
        if getattr(out, "path", None) == "-":
            yield out, template_py, {}
            return

        # out.path may be a pathlib.Path or string
        base = out.path
        try:
            from pathlib import Path

            basep = Path(base)
        except Exception:
            basep = base

        # Ensure the main runtime file uses the provided path as-is
        yield out, template_py, {}

        # Create a paired .pyi output next to the primary output
        try:
            pyi_path = basep.with_suffix(".pyi")
        except Exception:
            # If base is not path-like, append .pyi
            pyi_path = str(base) + ".pyi"

        yield OutputFile(pyi_path), template_pyi, {}
