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

"""Implementation of the Lydia backend."""
import shutil
from typing import Tuple

from pylogics.syntax.base import Formula
from pythomata.core import DFA
from pythomata.impl.symbolic import SymbolicDFA

from logaut.backends.base import Backend
from logaut.backends.common.process_mona_output import (
    parse_automaton,
    parse_mona_output,
)
from logaut.backends.lydia._lydia_utils import call_lydia, postprocess_lydia_output
from logaut.backends.lydia.to_lydia_grammar import to_string


class LydiaBackend(Backend):
    """The Lydia backend."""

    _LOWERBOUND_VERSION: Tuple[int, int, int] = (0, 1, 0)
    _UPPERBOUND_VERSION: Tuple[int, int, int] = (0, 2, 0)

    @classmethod
    def __check_lydia(cls):
        """Check that the Lydia CLI tool is available."""
        is_lydia_present = shutil.which("lydia") is not None
        if is_lydia_present is None:
            raise Exception(
                "Lydia binary is not installed. Please follow"
                "the installation instructions at https://github.com/whitemech/lydia.\n"
                "If instead it is installed, please check that it is in the system PATH."
            )
        # TODO: check Lydia version

    def __post_init__(self):
        """Do post-initialization checks."""
        self.__check_lydia()

    def ldl2dfa(self, formula: Formula) -> DFA:
        """From LDL to DFA."""
        return _process_formula(formula)

    def ltl2dfa(self, formula: Formula) -> DFA:
        """From LTL to DFA."""
        return _process_formula(formula)


def _process_formula(formula: Formula) -> SymbolicDFA:
    """
    Process a formula with Lydia.

    :param formula: the formula
    :return: the DFA
    """
    formula_str = to_string(formula)
    output = call_lydia(
        f"--logic={formula.logic.value}f", f"--inline={formula_str}", "-p"
    )
    mona_output_string = postprocess_lydia_output(output)
    mona_output = parse_mona_output(mona_output_string)
    automaton = parse_automaton(mona_output)
    return automaton
