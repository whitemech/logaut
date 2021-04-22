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

"""Transform a formula to a Lydia grammar."""
import functools

from pylogics.syntax.base import Formula, Not, Or
from pylogics.syntax.ltl import Always, StrongRelease, Until, WeakNext, WeakUntil
from pylogics.utils.to_string import to_string as pylogics_to_string


@functools.singledispatch
def to_string(formula: Formula):
    """
    Convert a formula to a Lydia-compliant formula.

    By default, use the Pylogics' 'to_string' function.
    """
    return pylogics_to_string(formula)


@to_string.register(WeakNext)
def to_string_weak_next(formula: WeakNext):
    """Transform the weaknext formula."""
    return f"W({formula.argument})"


@to_string.register(WeakUntil)
def to_string_weak_until(formula: WeakUntil):
    """Transform the 'weak until' formula."""

    def _translate_weak_until(left: Formula, right: Formula):
        return Or(Until(left, right), Always(right))

    result = _translate_weak_until(formula.operands[-1], formula.operands[-2])
    for sub_formula in reversed(formula.operands[:-2]):
        result = _translate_weak_until(sub_formula, result)
    return to_string(result)


@to_string.register(StrongRelease)
def to_string_strong_release(formula: StrongRelease) -> str:
    """
    Transform a strong release formula into string.

    Note that the strong release is not supported (yet) by Lydia.
    We reduce it to weak until by duality.
    """
    return to_string(Not(WeakUntil(*map(Not, formula.operands))))
