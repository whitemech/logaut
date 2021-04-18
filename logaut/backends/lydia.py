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

"""Implementation of the Lydia backend."""
import shutil

from logaut.backends.base import Backend


class LydiaBackend(Backend):
    """The Lydia backend."""

    @classmethod
    def __check_lydia_bin_available(cls):
        """Check that the Lydia CLI tool is available."""
        result = shutil.which("lydia")
        if result is None:
            raise Exception(
                "Lydia binary is not available. Please follow"
                "the installation instructions at https://github.com/whitemech/lydia."
            )

    def __post_init__(self):
        """Do post-initialization checks."""
        self.__check_lydia_bin_available()
