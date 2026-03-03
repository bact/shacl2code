#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
"""Language renderers"""

from pathlib import Path
from typing import Any, Callable, Dict, Type, TypeVar

LANGUAGES: Dict[str, Type[Any]] = {}

TEMPLATE_DIR = Path(__file__).parent / "templates"

T_Class = TypeVar("T_Class")


def language(name: str) -> Callable[[Type[T_Class]], Type[T_Class]]:
    """Decorator that registers a renderer class under the given language name."""

    def inner(cls: Type[T_Class]) -> Type[T_Class]:
        LANGUAGES[name] = cls
        return cls

    return inner
