#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT

import sys
import os
from contextlib import contextmanager
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateRuntimeError

from .lang import TEMPLATE_DIR


class OutputFile(object):
    def __init__(self, path):
        self.path = path

    @contextmanager
    def open(self):
        if self.path == "-":
            yield sys.stdout
        else:
            with open(self.path, "w") as f:
                yield f


class BasicJinjaRender(object):
    """
    Common Jinja Template Renderer

    Renderers that only use a single Jinja file can derive from this class. The
    class should set the class member variable `TEMPLATE` to indicate which
    template file to use. For example:

        @language("my-lang")
        class MyRendered(BasicJinjaRenderer):
            HELP = "Generates my-lang bindings"
            TEMPLATE = "my-lang.j2"

    """

    @classmethod
    def get_arguments(cls, parser):
        parser.add_argument(
            "--output",
            "-o",
            type=OutputFile,
            help="Output file or '-' for stdout",
            required=True,
        )

    def output(self, args, model):
        def abort_helper(msg):
            raise TemplateRuntimeError(msg)

        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        env.globals["abort"] = abort_helper
        template = env.get_template(self.TEMPLATE)

        render = template.render(
            disclaimer=f"This file was automatically generated by {os.path.basename(sys.argv[0])}. DO NOT MANUALLY MODIFY IT",
            enums=model.get_template_enums(),
            classes=model.get_template_classes(),
        )

        with args.output.open() as f:
            f.write(render)
