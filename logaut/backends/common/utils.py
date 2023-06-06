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

"""Common utility functions."""
import re

from pylogics.syntax.base import Formula

from logaut.backends.common.find_atoms.base import find_atoms


def _check_atoms_match_regex(formula: Formula, pattern: str, tool_name: str) -> None:
    atoms = find_atoms(formula)
    for atom in atoms:
        if re.fullmatch(pattern, atom) is None:
            raise ValueError(
                f"Atom '{atom}' is not a valid identifier. "
                f"{tool_name} only supports identifiers that match the regex " + pattern
            )
