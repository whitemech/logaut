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

"""Parse Lydia output to produce a pythomata.DFA."""

import re
from dataclasses import dataclass
from typing import Dict, Match, Set, Tuple, cast

from pythomata.impl.symbolic import SymbolicDFA
from sympy import And, Not, Or, Symbol, true
from sympy.logic.boolalg import BooleanFunction


@dataclass
class MONAOutput:
    """
    Dataclass to represent the MONA DFA output.

    See Section 2.4 of https://www.brics.dk/mona/mona14.pdf
    for more details.
    """

    nb_states: int
    variable_names: Tuple[str, ...]
    initial_state: int
    accepting_states: Set[int]
    rejecting_states: Set[int]
    transitions: Dict[int, Dict[int, Set[str]]]

    def __post_init__(self):
        """Do consistency checks after initialization."""
        assert 0 <= self.initial_state <= self.nb_states
        assert self.nb_states == self.initial_state + len(self.accepting_states) + len(
            self.rejecting_states
        )


@dataclass
class _MONAOutputWrapper:
    """A wrapper to the textual output of MONA."""

    output: str

    @property
    def variable_names(self) -> Tuple[str, ...]:
        """Get the variable names."""
        return tuple(
            cast(
                Match,
                re.search("DFA for formula with free variables: (.*)", self.output),
            )
            .group(1)
            .split()
        )

    @property
    def initial_state(self) -> int:
        """Get the initial state."""
        return int(
            cast(Match, re.search("Initial state: (.*)\n", self.output)).group(1)
        )

    @property
    def accepting_states(self) -> Set[int]:
        """Get the accepting states."""
        return set(
            map(
                int,
                cast(Match, re.search("Accepting states: (.*)\n", self.output))
                .group(1)
                .split(),
            )
        )

    @property
    def rejecting_states(self) -> Set[int]:
        """Get the rejecting states."""
        return set(
            map(
                int,
                cast(Match, re.search("Rejecting states: (.*)\n", self.output))
                .group(1)
                .split(),
            )
        )

    @property
    def nb_states(self) -> int:
        """Get the number of states."""
        return int(
            cast(
                Match,
                re.search(
                    r"Automaton has ([0-9]+) state(\(?s\)?)? and .* BDD-node(\(?s\)?)?",
                    self.output,
                ),
            ).group(1)
        )

    @property
    def raw_transitions(self) -> Dict[int, Dict[int, Set[str]]]:
        """
        Get the raw transitions.

        mapping: start state -> end state -> {guard to reach end from start}
        """
        raw_transitions: Dict[int, Dict[int, Set[str]]] = {}
        lines = self.output.splitlines()
        # from the 8th line, the output specifies the transitions.
        transition_strings = lines[7:]
        for t in transition_strings:
            match = cast(
                Match, re.search("State ([0-9]+): ([01X]+|) -> state ([0-9]+)", t)
            )
            if match is None:
                continue
            start_state = int(match.group(1))
            guard = match.group(2)
            end_state = int(match.group(3))
            raw_transitions.setdefault(start_state, {}).setdefault(
                end_state, set()
            ).add(guard)
        return raw_transitions


def parse_mona_output(dfa_output: str) -> MONAOutput:
    """
    Parse the MONA DFA output.

    :param dfa_output: the textual description of the MONA DFA.
    :return: a MONAOutput instance.
    """
    wrapper = _MONAOutputWrapper(dfa_output)
    variable_names: Tuple[str, ...] = wrapper.variable_names
    initial_state: int = wrapper.initial_state
    accepting_states: Set[int] = wrapper.accepting_states
    rejecting_states = wrapper.rejecting_states
    nb_states: int = wrapper.nb_states
    raw_transitions = wrapper.raw_transitions
    mona_output = MONAOutput(
        nb_states,
        variable_names,
        initial_state,
        accepting_states,
        rejecting_states,
        raw_transitions,
    )
    return mona_output


def from_set_of_guards_to_sympy_formula(
    guards: Set[str], variable_names: Tuple[str, ...]
) -> BooleanFunction:
    """
    Compute the SymPy formula from MONA guards.

    MONA guards are strings of only '0', '1' and 'X'.
    Character ith indicates the truth value required
    for the ith proposition: '0' stands for false,
    '1' stands for true, and 'X' stands for "don't care".

    A set of MONA guards is intended to be in disjunction.

    :param guards: the set of MONA guards.
    :param variable_names: the variable names.
    :return: the SymPy boolean function associated with the set of guards.
    """

    def _index_value_pair_to_literal(pair):
        index, value = pair
        value = bool(int(value))
        literal = Symbol(variable_names[index])
        return literal if value else Not(literal)

    processed_guards = []
    for guard in guards:
        if guard == "":
            processed_guards.append(true)
        else:
            filtered_guard = list(filter(lambda x: x[1] != "X", enumerate(guard)))
            clause = And(*map(_index_value_pair_to_literal, filtered_guard))
            processed_guards.append(clause)
    result = Or(*processed_guards)
    return result


def parse_automaton(output: MONAOutput) -> SymbolicDFA:
    """
    Build a pythomata.SymbolicDFA, given the MONAOutput object.

    :param output: a MONAOutput instance.
    :return: the (symbolic) DFA.
    """
    automaton = SymbolicDFA()

    # create states, set initial state and set accepting states.
    automaton.set_accepting_state(0, 0 in output.accepting_states)
    automaton.set_initial_state(0)
    for _ in range(1, output.nb_states):
        current_state = automaton.create_state()
        automaton.set_accepting_state(
            current_state, current_state in output.accepting_states
        )

    # populate transitions.
    for start_state, outgoing_transitions in output.transitions.items():
        for end_state, guards in outgoing_transitions.items():
            symbolic_guard = from_set_of_guards_to_sympy_formula(
                guards, output.variable_names
            )
            automaton.add_transition((start_state, symbolic_guard, end_state))
    return automaton
