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

"""This module implements the library exceptions."""


class LogautException(Exception):
    """Base library exception."""


class NotImplementedBackendFunction(LogautException):
    """Raise this exception when a backend does not support an operation."""


class BadLogicFormulaException(LogautException):
    """Raise this exception when the ."""

    __ERROR_MSG = "wrong formula for method {method_name}: expected formalism '{expected}', found '{actual}'"

    def __init__(self, method_name: str, expected: str, actual: str, *args, **kwargs):
        """Initialize the exception."""
        format_args = dict(method_name=method_name, expected=expected, actual=actual)
        super().__init__(self.__ERROR_MSG.format(**format_args))
