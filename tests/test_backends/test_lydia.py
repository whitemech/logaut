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
import re

from hypothesis import HealthCheck, assume, given, settings
from hypothesis.extra.lark import from_lark
from pylogics.parsers.ldl import __parser as ldl_parser
from pylogics.parsers.ldl import parse_ldl
from pylogics.parsers.ltl import __parser as ltl_parser
from pylogics.parsers.ltl import parse_ltl
from pylogics.syntax.base import Formula
from pythomata.core import DFA

from logaut.backends.common.find_atoms.base import find_atoms
from logaut.backends.lydia.core import _LYDIA_SYMBOL_REGEX
from logaut.core import ldl2dfa, ltl2dfa

lydia_hypothesis_settings = settings(
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=10_000,
    max_examples=1_000,
)


def skip_if_for_lydia(formula: Formula) -> None:
    """Skip test if formula might not be acceptable by the lydia parser."""
    atoms = find_atoms(formula)
    for atom in atoms:
        assume(re.fullmatch(_LYDIA_SYMBOL_REGEX, atom) is not None)


@lydia_hypothesis_settings
@given(from_lark(ldl_parser._parser))
def test_lydia_backend_ldl(formula_str):
    """Test lydia backend for LDL formulae."""
    assume(formula_str.isascii())
    assume(formula_str != "last")
    assume(formula_str != "end")
    formula = parse_ldl(formula_str)
    skip_if_for_lydia(formula)
    output = ldl2dfa(formula, backend="lydia")
    assert isinstance(output, DFA)


@lydia_hypothesis_settings
@given(from_lark(ltl_parser._parser))
def test_lydia_backend_ltl(formula_str):
    """Test lydia backend for LTL formulae."""
    formula = parse_ltl(formula_str)
    skip_if_for_lydia(formula)
    output = ltl2dfa(formula, backend="lydia")
    assert isinstance(output, DFA)
