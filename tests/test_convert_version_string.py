#
# Copyright (c) 2026 Joshua Watt
#
# SPDX-License-Identifier: MIT

import pytest

from shacl2code.util import convert_version_string


def p(string, value):
    return pytest.param(string, value, id=string)


@pytest.mark.parametrize(
    "string,value",
    [
        p("1.0.0", (1, 0, 0)),
        p(".0.0", ("", 0, 0)),
        p("1", (1,)),
        p("-1.0.-10", ("-1", 0, "-10")),
        p("0x01.0.0b11", ("0x01", 0, "0b11")),
        p("+1.0", ("+1", 0)),
        p("1.alpha", (1, "alpha")),
        p("", tuple()),
        p(".", ("", "")),
        p("alpha.0", ("alpha", 0)),
        p("-1suffix", ("-1suffix",)),
        p("+1suffix", ("+1suffix",)),
    ],
)
def test_convert_version_string(string, value):
    assert convert_version_string(string) == value
