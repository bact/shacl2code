#! /usr/bin/env python3
#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .context import Context


@dataclass
class ContextData:
    """Holds a JSON-LD context dict and the URL it was fetched from."""

    context: Dict[str, Any]
    url: str


class UrlContext(Context):
    """A Context that tracks the source URLs of each context."""

    def __init__(self, contexts: Optional[List[ContextData]] = None) -> None:
        if contexts is None:
            contexts = []  # pragma: no cover

        super().__init__([c.context.get("@context", {}) for c in contexts])
        self.urls: List[str] = []
        for ctx in contexts:
            self.urls.append(ctx.url)
