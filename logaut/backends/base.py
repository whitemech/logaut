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

"""Abstract definition of a backend."""
import inspect
import re
from abc import ABC, ABCMeta
from enum import Enum
from functools import wraps
from operator import attrgetter

from pylogics.syntax.base import Formula
from pythomata.core import DFA

from logaut.exceptions import BadLogicFormulaException, NotImplementedBackendFunction


class _Logics(Enum):
    LTL = "ltl"
    PLTL = "pltl"
    LDL = "ldl"
    PLDL = "pldl"
    FOL = "fol"
    MSO = "mso"


class _MetaBackend(ABCMeta):
    """Metaclass for backends."""

    method_name_regex = re.compile(
        rf"({'|'.join(map(attrgetter('value'), _Logics))})2dfa"
    )

    @classmethod
    def _add_validation(mcs, func):
        """Add validation."""
        name = func.__name__
        match = mcs.method_name_regex.fullmatch(name)
        if match is None:
            return func
        logic_name = match.group(1)

        @wraps(func)
        def validate(self, formula: Formula) -> DFA:
            """Validate the input formula to be of the right logic formalism."""
            expected_logic_name = logic_name
            actual_logic_name = formula.logic.value
            if actual_logic_name != expected_logic_name:
                raise BadLogicFormulaException(
                    name, expected_logic_name, actual_logic_name
                )
            return func(self, formula)

        return validate

    def __new__(mcs, *args, **kwargs):
        """
        Instantiate a new class.

        Add formula validation before each method call.
        """
        class_ = super().__new__(mcs, *args, **kwargs)
        methods = inspect.getmembers(class_, predicate=inspect.ismethod)
        for method_name, method_obj in methods:
            setattr(class_, method_name, mcs._add_validation(method_obj))
        return class_


class Backend(ABC, metaclass=_MetaBackend):
    """Logaut back-end interface."""

    @classmethod
    def __not_supported_error(cls, operation: str) -> Exception:
        """Raise a not supported error."""
        return NotImplementedBackendFunction(
            f"operation '{operation}' is not supported by backend '{cls.__name__}'"
        )

    def ltl2dfa(self, formula: Formula) -> DFA:
        """
        Transform an LTL formula into a DFA.

        :param formula: an LTL formula
        :return: the equivalent DFA
        """
        raise self.__not_supported_error(self.ltl2dfa.__name__)

    def ldl2dfa(self, formula: Formula) -> DFA:
        """
        Transform an LDL formula into a DFA.

        :param formula: an LDL formula
        :return: the equivalent DFA
        """
        raise self.__not_supported_error(self.ldl2dfa.__name__)

    def pltl2dfa(self, formula: Formula) -> DFA:
        """
        Transform a PLTL formula into a DFA.

        :param formula: a PLTL formula
        :return: the equivalent DFA
        """
        raise self.__not_supported_error(self.pltl2dfa.__name__)

    def pldl2dfa(self, formula: Formula) -> DFA:
        """
        Transform a PLDL formula into a DFA.

        :param formula: a PLDL formula
        :return: the equivalent DFA
        """
        raise self.__not_supported_error(self.pldl2dfa.__name__)

    def fol2dfa(self, formula: Formula) -> DFA:
        """
        Transform a FOL formula into a DFA.

        :param formula: a FOL formula
        :return: the equivalent DFA
        """
        raise self.__not_supported_error(self.fol2dfa.__name__)

    def mso2dfa(self, formula: Formula) -> DFA:
        """
        Transform a MSO formula into a DFA.

        :param formula: a MSO formula
        :return: the equivalent DFA
        """
        raise self.__not_supported_error(self.mso2dfa.__name__)
