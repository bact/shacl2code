# SPDX-FileCopyrightText: Copyright (c) 2024 Joshua Watt
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT

import sys
import os
from pathlib import Path
from contextlib import contextmanager
import jinja2
from jinja2 import Environment, FileSystemLoader, TemplateRuntimeError
from markupsafe import Markup
from rdflib.namespace import SH
from ..model import SHACL2CODE
from ..version import VERSION

THIS_DIR = Path(__file__).parent


class OutputFile(object):
    def __init__(self, path):
        self.path = path

    @contextmanager
    def open(self, mode):
        if self.path == "-":
            yield sys.stdout
        else:
            with open(self.path, "w") as f:
                yield f


@jinja2.pass_context
def include_file(ctx, name):
    env = ctx.environment
    return Markup(env.loader.get_source(env, name)[0])


class JinjaTemplateRender(object):
    def __init__(self, args):
        self.spdx_license = args.license

    def get_additional_render_args(self):
        return {}

    def get_extra_env(self):
        return {}

    def render(self, template, output, *, extra_env={}, render_args={}):
        def abort_helper(msg):
            raise TemplateRuntimeError(msg)

        env = Environment(loader=FileSystemLoader([template.parent, THIS_DIR.parent]))
        for k, v in extra_env.items():
            env.globals[k] = v
        env.globals["abort"] = abort_helper
        env.globals["SHACL2CODE"] = SHACL2CODE
        env.globals["SH"] = SH
        env.globals["SHACL2CODE_VERSION"] = VERSION
        template = env.get_template(template.name)

        render = template.render(
            disclaimer=f"This file was automatically generated by {os.path.basename(sys.argv[0])}. DO NOT MANUALLY MODIFY IT",
            spdx_license=self.spdx_license,
            **render_args,
        )

        output.write(render)
        if not render[-1] == "\n":
            output.write("\n")

    def output(self, model):
        """
        Render the provided model
        """

        class ObjectList(object):
            def __init__(self, objs):
                self.__objs = objs

            def __iter__(self):
                return iter(self.__objs)

            def get(self, _id):
                for o in self.__objs:
                    if o._id == _id:
                        return o
                raise KeyError(f"Object with ID {_id} not found")

        def get_all_derived(cls):
            def _recurse(cls):
                result = set(cls.derived_ids)
                for r in cls.derived_ids:
                    result |= _recurse(classes.get(r))
                return result

            d = list(_recurse(cls))
            d.sort()
            return d

        def get_all_named_individuals(cls):
            ni = set(i._id for i in cls.named_individuals)

            for d in get_all_derived(cls):
                ni |= set(i._id for i in classes.get(d).named_individuals)

            ni = list(ni)
            ni.sort()
            return ni

        classes = ObjectList(model.classes)
        concrete_classes = ObjectList(
            list(c for c in model.classes if not c.is_abstract)
        )
        abstract_classes = ObjectList(list(c for c in model.classes if c.is_abstract))
        enums = ObjectList(model.enums)

        render_args = {
            "classes": classes,
            "concrete_classes": concrete_classes,
            "abstract_classes": abstract_classes,
            "enums": enums,
            "context": model.context,
            **self.get_additional_render_args(),
        }

        env = {
            "get_all_derived": get_all_derived,
            "get_all_named_individuals": get_all_named_individuals,
            "include_file": include_file,
            **self.get_extra_env(),
        }

        for output, template, args in self.get_outputs():
            with output.open("w") as f:
                self.render(
                    template,
                    f,
                    extra_env=env,
                    render_args={**render_args, **args},
                )


class BasicJinjaRender(JinjaTemplateRender):
    """
    Common Jinja Template Renderer

    Renderers that only use a single Jinja file can derive from this class. For
    example:

        @language("my-lang")
        class MyRendered(BasicJinjaRenderer):
            HELP = "Generates my-lang bindings"

            def __init__(self, args):
                super().__init__(args, PATH / TO / TEMPLATE)
    """

    def __init__(self, args, template):
        super().__init__(args)
        self.__output = args.output
        self.__template = template

    @classmethod
    def get_arguments(cls, parser):
        parser.add_argument(
            "--output",
            "-o",
            type=OutputFile,
            help="Output file or '-' for stdout",
            required=True,
        )

    def get_outputs(self):
        yield self.__output, self.__template, {}
