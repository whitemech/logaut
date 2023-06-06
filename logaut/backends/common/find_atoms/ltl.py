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
from typing import Set

from pylogics.syntax.ltl import PropositionalFalse, PropositionalTrue

from logaut.backends.common.find_atoms.base import find_atoms


@find_atoms.register
def _(formula: PropositionalTrue) -> Set[str]:
    """No atomic propositions in a propositional true."""
    return set()


@find_atoms.register
def _(formula: PropositionalFalse) -> Set[str]:
    """No atomic propositions in a propositional false."""
    return set()
