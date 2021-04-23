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
from typing import Match, Tuple, cast

import ltlf2dfa
from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.parser.pltlf import PLTLfParser
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
        is_right_version = ltlf2dfa.__version__ == "1.0.1"
        if not is_right_version:
            raise Exception(
                "LTLf2DFA needs to be at version 1.0.1. "
                "Please install it manually using:"
                "\n"
                "\tpip install git+https://github.com/whitemech/LTLf2DFA.git@develop#egg=ltlf2dfa"
            )

    def __post_init__(self):
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
    mona_output = parse_mona_output(postprocess_output(mona_output_string))
    automaton = parse_automaton(mona_output)
    return automaton


def postprocess_output(output: str) -> str:
    """
    Post-process MONA output.

    Capture the output related to the MONA DFA transitions.

    :param: the raw output from the LTLf2DFA tool.
    :return: the output associated to the DFA.
    """
    regex = re.compile(
        r".*(?=\nFormula is (valid|unsatisfiable)|A counter-example)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = regex.search(output)
    if match is None:
        raise Exception("cannot find automaton description in MONA output.")
    return cast(Match, regex.search(output)).group(0)
