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

"""Find atomic propositions from a Pylogics formula."""
import operator
from functools import reduce, singledispatch
from typing import Set

from pylogics.syntax.base import (
    AbstractAtomic,
    FalseFormula,
    Formula,
    TrueFormula,
    _BinaryOp,
    _UnaryOp,
)


@singledispatch
def find_atoms(formula: Formula) -> Set[str]:
    """Find all atomic propositions in a formula."""
    raise NotImplementedError(f"Don't know how to handle {type(formula)}")


@find_atoms.register
def _(formula: AbstractAtomic) -> Set[str]:
    """Find all atomic propositions in an atomic proposition."""
    return {formula.name}


@find_atoms.register
def _(formula: _UnaryOp) -> Set[str]:
    """Find all atomic propositions in a Pylogics unary operation."""
    return find_atoms(formula.argument)


@find_atoms.register
def _(formula: _BinaryOp) -> Set[str]:
    """Find all atomic propositions in an Pylogics binary operation."""
    return reduce(operator.or_, map(find_atoms, formula.operands))


@find_atoms.register
def _(formula: TrueFormula) -> Set[str]:
    """Return empty since no atomic propositions in a boolean constant true."""
    return set()


@find_atoms.register
def _(formula: FalseFormula) -> Set[str]:
    """Return empty since no atomic propositions in a boolean constant true."""
    return set()
