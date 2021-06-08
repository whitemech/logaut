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

"""This module contains utilities to call the Lydia tool from Python."""
import re
import subprocess
from typing import Match, cast

from pylogics.helpers.misc import enforce

from logaut.exceptions import LogautException


def call_lydia(*args) -> str:
    """Call the Lydia CLI tool with the arguments provided."""
    command = ["lydia", *args]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        stderr = result.stderr.decode()
        enforce(result.returncode == 0, exception_cls=LogautException)
        return output
    except LogautException:
        raise Exception(  # type: ignore
            f"the Lydia command {' '.join(command)} failed.\nstdout={output}\nstderr={stderr}"  # type: ignore
        )
    except Exception as e:
        raise Exception(f"an error occurred while running lydia: {str(e)}") from e


def postprocess_lydia_output(output: str) -> str:
    """
    Post-process Lydia output.

    Capture the output related to the MONA DFA transitions.

    :param: the raw output of the Lydia CLI tool.
    :return: the output associated to the DFA.
    """
    regex = re.compile(
        r"(?<=Computed automaton:\n).*(?=\n\[2)", flags=re.MULTILINE | re.DOTALL
    )
    match = regex.search(output)
    if match is None:
        raise Exception("cannot find automaton description in Lydia output.")
    return cast(Match, regex.search(output)).group(0)
