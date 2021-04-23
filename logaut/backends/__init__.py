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

"""
Backends for logaut.

This subpackage contains backend abstract definitions
and some of its implementations.
"""
from logaut._registry import Registry
from logaut.backends.base import Backend

_backend_registry = Registry[Backend]()


def register(*args, **kwargs) -> None:
    """Register a backend."""
    _backend_registry.register(*args, **kwargs)


def make(*args, **kwargs) -> Backend:
    """Instantiate a backend."""
    return _backend_registry.make(*args, **kwargs)


register(id_="lydia", entry_point="logaut.backends.lydia.core:LydiaBackend")
register(id_="ltlf2dfa", entry_point="logaut.backends.ltlf2dfa.core:LTLf2DFABackend")
