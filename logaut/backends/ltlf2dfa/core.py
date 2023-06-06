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

"""
Implementation of the LTLf2DFA backend.

Repository:

    https://github.com/whitemech/LTLf2DFA/

"""
import re
import shutil
from functools import singledispatch
from typing import Match, Set, Tuple, cast

import ltlf2dfa
from ltlf2dfa.base import AtomicFormula, BinaryOperator
from ltlf2dfa.base import Formula as LTLf2DFAFormula
from ltlf2dfa.base import UnaryOperator
from ltlf2dfa.ltlf import LTLfFalse, LTLfFormula, LTLfTrue
from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.parser.pltlf import PLTLfParser
from ltlf2dfa.pltlf import PLTLfFalse, PLTLfTrue
from pylogics.syntax.base import Formula, Logic
from pythomata.core import DFA
from pythomata.impl.symbolic import SymbolicDFA

from logaut.backends.base import Backend
from logaut.backends.common.process_mona_output import (
    parse_automaton,
    parse_mona_output,
)
from logaut.backends.ltlf2dfa.to_ltlf2dfa_formula import to_string


class LTLf2DFABackend(Backend):
    """The LTLf2DFA backend."""

    _LOWERBOUND_VERSION: Tuple[int, int, int] = (0, 1, 0)
    _UPPERBOUND_VERSION: Tuple[int, int, int] = (0, 2, 0)

    @classmethod
    def __check_mona(cls):
        """Check that the MONA CLI tool is available."""
        is_mona_present = shutil.which("mona") is not None
        if is_mona_present is None:
            raise Exception(
                "MONA binary is not installed. Please follow"
                "the installation instructions at https://github.com/whitemech/MONA.\n"
                "If instead it is installed, please check that it is in the system PATH."
            )

    @classmethod
    def __check_ltlf2dfa(cls):
        """Check that the LTLf2DFA package is at the right version."""
        is_right_version = ltlf2dfa.__version__ == "1.0.2"
        if not is_right_version:
            raise Exception("LTLf2DFA needs to be at version 1.0.2.")

    def init_checks(self) -> None:
        """Do post-initialization checks."""
        self.__check_mona()
        self.__check_ltlf2dfa()

    def ltl2dfa(self, formula: Formula) -> DFA:
        """From LTL to DFA."""
        return _process_formula(formula)

    def pltl2dfa(self, formula: Formula) -> DFA:
        """From PLTL to DFA."""
        return _process_formula(formula)


def _process_formula(formula: Formula) -> SymbolicDFA:
    """
    Process a formula with Lydia.

    :param formula: the formula
    :return: the DFA
    """
    logic = formula.logic
    formula_str = to_string(formula)
    parser = LTLfParser() if logic == Logic.LTL else PLTLfParser()
    ltlf2dfa_formula = parser(formula_str)
    mona_output_string = ltlf2dfa_formula.to_dfa(mona_dfa_out=True)
    mona_output = parse_mona_output(
        postprocess_output(mona_output_string, ltlf2dfa_formula)
    )
    automaton = parse_automaton(mona_output)
    return automaton


def postprocess_output(output: str, formula: LTLfFormula) -> str:
    """
    Post-process MONA output.

    Capture the output related to the MONA DFA transitions.

    :param output: the raw output from the LTLf2DFA tool.
    :param formula: the formula
    :return: the output associated to the DFA.
    """
    # hotfix: remove uppercased symbols
    propositions = get_atomic_propositions(formula)
    for proposition in propositions:
        upper = proposition.upper()
        output = re.sub(f"(?<=\n ){upper}(?= =)", proposition, output)

    regex = re.compile(
        r".*(?=\nFormula is (valid|unsatisfiable)|A counter-example)",
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    match = regex.search(output)
    if match is None:
        raise Exception("cannot find automaton description in MONA output.")
    return cast(Match, regex.search(output)).group(0)


@singledispatch
def get_atomic_propositions(formula: LTLf2DFAFormula) -> Set[str]:
    """
    Get the set of all atomic propositions in the PPLTL/LTLf formula.

    :param formula: a PLTL/LTLfFormula instance.
    :return: a set of all atomic propositions.
    """
    raise NotImplementedError("Unsupported formula type")


@get_atomic_propositions.register
def _(formula: AtomicFormula) -> Set[str]:
    """Return its symbol if the formula is an atomic proposition."""
    return {formula.s}  # Assuming 's' is the symbol of the atomic proposition


@get_atomic_propositions.register
def _(formula: LTLfTrue) -> Set[str]:
    """Return empty if the formula is a boolean constant."""
    return set()


@get_atomic_propositions.register
def _(formula: LTLfFalse) -> Set[str]:
    """Return empty if the formula is a boolean constant."""
    return set()


@get_atomic_propositions.register
def _(formula: PLTLfTrue) -> Set[str]:
    """Return empty if the formula is a boolean constant."""
    return set()


@get_atomic_propositions.register
def _(formula: PLTLfFalse) -> Set[str]:
    """Return empty if the formula is a boolean constant."""
    return set()


@get_atomic_propositions.register
def _(formula: UnaryOperator) -> Set[str]:
    # If the formula is a unary operator, recursively call for its child
    return get_atomic_propositions(formula.f)


@get_atomic_propositions.register
def _(formula: BinaryOperator) -> Set[str]:
    # If the formula is a binary operator, recursively call for its children and union the results
    return set().union(*(get_atomic_propositions(f) for f in formula.formulas))
