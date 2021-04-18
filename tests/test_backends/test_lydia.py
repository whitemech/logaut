# -*- coding: utf-8 -*-
#
# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of logaut.
#
# logaut is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# logaut is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with logaut.  If not, see <https://www.gnu.org/licenses/>.
#

"""Tests for Lydia backend."""
from hypothesis import given
from hypothesis.extra.lark import from_lark
from pylogics.parsers.ldl import __parser, parse_ldl
from pythomata.core import DFA

from logaut.core import ldl2dfa
from tests.conftest import suppress_health_checks_for_lark


@suppress_health_checks_for_lark
@given(from_lark(__parser._parser))
def test_lydia_backend(formula_str):
    """Test lydia backend."""
    formula = parse_ldl(formula_str)
    output = ldl2dfa(formula, backend="lydia")
    assert isinstance(output, DFA)
