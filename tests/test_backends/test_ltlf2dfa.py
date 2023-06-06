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

"""Tests for LTLf2DFA backend."""
import re

from hypothesis import HealthCheck, assume, given, settings
from hypothesis.extra.lark import from_lark
from pylogics.parsers.ltl import __parser as ltl_parser
from pylogics.parsers.ltl import parse_ltl
from pylogics.parsers.pltl import __parser as pltl_parser
from pylogics.parsers.pltl import parse_pltl
from pylogics.syntax.base import Formula
from pythomata.core import DFA

from logaut import ltl2dfa, pltl2dfa
from logaut.backends.common.find_atoms.base import find_atoms
from logaut.backends.ltlf2dfa.core import _LTLf2DFA_SYMBOL_REGEX

ltlf2dfa_hypothesis_settings = settings(
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=1_000,
    max_examples=1_000,
)


def skip_if_for_ltlf2dfa(formula: Formula) -> None:
    """Skip test if formula might not be acceptable by the ltlf2dfa parser."""
    atoms = find_atoms(formula)
    for atom in atoms:
        assume(re.fullmatch(_LTLf2DFA_SYMBOL_REGEX, atom) is not None)


@ltlf2dfa_hypothesis_settings
@given(from_lark(ltl_parser._parser))
def test_ltlf2dfa_backend_ltl(formula_str):
    """Test ltlf2dfa backend for LTL."""
    formula = parse_ltl(formula_str)
    skip_if_for_ltlf2dfa(formula)
    output = ltl2dfa(formula, backend="ltlf2dfa")
    assert isinstance(output, DFA)


@ltlf2dfa_hypothesis_settings
@given(from_lark(pltl_parser._parser))
def test_ltlf2dfa_backend_pltl(formula_str):
    """Test lydia backend for PLTL."""
    formula = parse_pltl(formula_str)
    skip_if_for_ltlf2dfa(formula)
    output = pltl2dfa(formula, backend="ltlf2dfa")
    assert isinstance(output, DFA)
