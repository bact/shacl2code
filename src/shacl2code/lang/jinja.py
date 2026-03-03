#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""Jinja template renderer (for testing)"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from .common import BasicJinjaRender
from .lang import language

if TYPE_CHECKING:
    import argparse


@language("jinja")
class JinjaRender(BasicJinjaRender):
    """Render Jinja Output (for testing)."""

    HELP = "Render Jinja Output (for testing)"

    def __init__(self, args: Any) -> None:
        super().__init__(args, args.template)

    @classmethod
    def get_arguments(cls, parser: "argparse.ArgumentParser") -> None:
        super().get_arguments(parser)

        parser.add_argument(
            "--template",
            "-t",
            type=Path,
            help="Jinja Template file",
            required=True,
        )
