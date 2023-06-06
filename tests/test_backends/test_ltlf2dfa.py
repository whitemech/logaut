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
from hypothesis import HealthCheck, assume, given, settings
from hypothesis.extra.lark import from_lark
from pylogics.parsers.ltl import __parser as ltl_parser
from pylogics.parsers.ltl import parse_ltl
from pylogics.parsers.pltl import __parser as pltl_parser
from pylogics.parsers.pltl import parse_pltl
from pythomata.core import DFA

from logaut.core import ltl2dfa, pltl2dfa

ltlf2dfa_hypothesis_settings = settings(
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=1_000,
    max_examples=1_000,
)


def skip_if_with_quotes(formula_str: str) -> None:
    """Skip test if formula might not be acceptable by the ltlf2dfa parser."""
    assume(formula_str.islower() and '"' not in formula_str and "_" not in formula_str)


@ltlf2dfa_hypothesis_settings
@given(from_lark(ltl_parser._parser))
def test_ltlf2dfa_backend_ltl(formula_str):
    """Test ltlf2dfa backend for LTL."""
    skip_if_with_quotes(formula_str)
    formula = parse_ltl(formula_str)
    output = ltl2dfa(formula, backend="ltlf2dfa")
    assert isinstance(output, DFA)


@ltlf2dfa_hypothesis_settings
@given(from_lark(pltl_parser._parser))
def test_ltlf2dfa_backend_pltl(formula_str):
    """Test lydia backend for PLTL."""
    skip_if_with_quotes(formula_str)
    formula = parse_pltl(formula_str)
    output = pltl2dfa(formula, backend="ltlf2dfa")
    assert isinstance(output, DFA)
