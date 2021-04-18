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

"""Helpers module."""

import re


class RegexConstrainedString(str):
    """
    A string that is constrained by a regex.

    The default behaviour is to match anything.
    Subclass this class and change the 'REGEX' class
    attribute to implement a different behaviour.
    """

    REGEX = re.compile(".*", flags=re.DOTALL)

    def __new__(cls, value, *args, **kwargs):
        """Instantiate a new object."""
        if type(value) == cls:
            return value
        inst = super(RegexConstrainedString, cls).__new__(cls, value)
        return inst

    def __init__(self, *_, **__):
        """Initialize a regex constrained string."""
        super().__init__()
        if not self.REGEX.fullmatch(self):
            self._handle_no_match()

    def _handle_no_match(self):
        raise ValueError(
            "Value '{data}' does not match the regular expression {regex}".format(
                data=self, regex=self.REGEX
            )
        )
