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

"""Transform a formula to a LTLf2DFA grammar."""

import functools
from typing import Sequence

from pylogics.syntax.base import (
    AbstractAtomic,
    And,
    Equivalence,
    FalseFormula,
    Formula,
    Implies,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ltl import (
    Always,
    Eventually,
    Next,
    Release,
    StrongRelease,
    Until,
    WeakNext,
    WeakUntil,
)
from pylogics.utils.to_string import to_string as pylogics_to_string


@functools.singledispatch
def to_string(formula: Formula) -> str:
    """Transform a formula to a parsable string."""
    return pylogics_to_string(formula)


def _map_operands_to_string(operands: Sequence[Formula]):
    """Map a list of operands to a list of strings (with brackets)."""
    return map(lambda sub_formula: f"({to_string(sub_formula)})", operands)


@to_string.register(And)
def to_string_and(formula: And) -> str:
    """Transform an And into string."""
    return " & ".join(_map_operands_to_string(formula.operands))


@to_string.register(Or)
def to_string_or(formula: Or) -> str:
    """Transform an Or into string."""
    return " | ".join(_map_operands_to_string(formula.operands))


@to_string.register(Not)
def to_string_not(formula: Not) -> str:
    """Transform a Not into string."""
    return f"~({to_string(formula.argument)})"


@to_string.register(Implies)
def to_string_implies(formula: Implies) -> str:
    """Transform an Implies into string."""
    return " -> ".join(_map_operands_to_string(formula.operands))


@to_string.register(Equivalence)
def to_string_equivalence(formula: Equivalence) -> str:
    """Transform an Equivalence into string."""
    return " <-> ".join(_map_operands_to_string(formula.operands))


@to_string.register(AbstractAtomic)
def to_string_atomic(formula: AbstractAtomic) -> str:
    """Transform an atomic formula into string."""
    return formula.name


@to_string.register(TrueFormula)
def to_string_true(_formula: TrueFormula) -> str:
    """Transform the "true" formula into string."""
    return "true"


@to_string.register(FalseFormula)
def to_string_false(_formula: FalseFormula) -> str:
    """Transform the "false" formula into string."""
    return "false"


@to_string.register(Next)
def to_string_next(formula: Next) -> str:
    """Transform a next formula into string."""
    return f"X({to_string(formula.argument)})"


@to_string.register(WeakNext)
def to_string_weak_next(formula: WeakNext) -> str:
    """Transform a weak next formula into string."""
    return f"WX({to_string(formula.argument)})"


@to_string.register(Until)
def to_string_until(formula: Until) -> str:
    """Transform a until formula into string."""
    return " U ".join(_map_operands_to_string(formula.operands))


@to_string.register(WeakUntil)
def to_string_weak_until(formula: WeakUntil):
    """Transform the 'weak until' formula."""

    def _translate_weak_until(left: Formula, right: Formula):
        return Or(Until(left, right), Always(right))

    result = _translate_weak_until(formula.operands[-1], formula.operands[-2])
    for sub_formula in reversed(formula.operands[:-2]):
        result = _translate_weak_until(sub_formula, result)
    return to_string(result)


@to_string.register(Release)
def to_string_release(formula: Release) -> str:
    """Transform a release formula into string."""
    return " R ".join(_map_operands_to_string(formula.operands))


@to_string.register(StrongRelease)
def to_string_strong_release(formula: StrongRelease) -> str:
    """
    Transform a strong release formula into string.

    Note that the strong release is not supported (yet) by LTLf2DFA.
    We reduce it to weak until by duality.
    """
    result = to_string(WeakUntil(*map(Not, formula.operands)))
    return f"!({result})"


@to_string.register(Eventually)
def to_string_eventually(formula: Eventually) -> str:
    """Transform a eventually formula into string."""
    return f"F({to_string(formula.argument)})"


@to_string.register(Always)
def to_string_always(formula: Always) -> str:
    """Transform a always formula into string."""
    return f"G({to_string(formula.argument)})"
