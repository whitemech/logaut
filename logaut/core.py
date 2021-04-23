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

"""Logaut core module."""
from pylogics.syntax.base import Formula
from pythomata.core import DFA

import logaut.backends

_DEFAULT_BACKEND = "lydia"


def _call_method(
    formula: Formula, backend_id: str, method_name: str, **backend_options
) -> DFA:
    """Call a method."""
    backend = logaut.backends.make(backend_id, **backend_options)
    method = getattr(backend, method_name)
    return method(formula)


def ltl2dfa(
    formula: Formula, backend: str = _DEFAULT_BACKEND, **backend_options
) -> DFA:
    """
    From LTL to DFA.

    :param formula: the formula to translate.
    :param backend: the backend to use.
    :param backend_options: options to pass to the backend.
    :return: the DFA.
    """
    return _call_method(formula, backend, ltl2dfa.__name__, **backend_options)


def ldl2dfa(
    formula: Formula, backend: str = _DEFAULT_BACKEND, **backend_options
) -> DFA:
    """
    From LDL to DFA.

    :param formula: the formula to translate.
    :param backend: the backend to use.
    :param backend_options: options to pass to the backend.
    :return: the DFA.
    """
    return _call_method(formula, backend, ldl2dfa.__name__, **backend_options)


def pltl2dfa(
    formula: Formula, backend: str = _DEFAULT_BACKEND, **backend_options
) -> DFA:
    """
    From PLTL to DFA.

    :param formula: the formula to translate.
    :param backend: the backend to use.
    :param backend_options: options to pass to the backend.
    :return: the DFA.
    """
    return _call_method(formula, backend, pltl2dfa.__name__, **backend_options)


def pldl2dfa(
    formula: Formula, backend: str = _DEFAULT_BACKEND, **backend_options
) -> DFA:
    """
    From PLDL to DFA.

    :param formula: the formula to translate.
    :param backend: the backend to use.
    :param backend_options: options to pass to the backend.
    :return: the DFA.
    """
    return _call_method(formula, backend, pldl2dfa.__name__, **backend_options)


def fol2dfa(
    formula: Formula, backend: str = _DEFAULT_BACKEND, **backend_options
) -> DFA:
    """
    From FOL to DFA.

    :param formula: the formula to translate.
    :param backend: the backend to use.
    :param backend_options: options to pass to the backend.
    :return: the DFA.
    """
    return _call_method(formula, backend, fol2dfa.__name__, **backend_options)


def mso2dfa(
    formula: Formula, backend: str = _DEFAULT_BACKEND, **backend_options
) -> DFA:
    """
    From MSO to DFA.

    :param formula: the formula to translate.
    :param backend: the backend to use.
    :param backend_options: options to pass to the backend.
    :return: the DFA.
    """
    return _call_method(formula, backend, mso2dfa.__name__, **backend_options)
