<h1 align="center">
  <b>logaut</b>
</h1>

<p align="center">
  <a href="https://pypi.org/project/logaut">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/logaut">
  </a>
  <a href="https://pypi.org/project/logaut">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/logaut" />
  </a>
  <a href="">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/logaut" />
  </a>
  <a href="">
    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/logaut">
  </a>
  <a href="">
    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/logaut">
  </a>
  <a href="https://github.com/whitemech/logaut/blob/master/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/marcofavorito/logaut">
  </a>
</p>
<p align="center">
  <a href="">
    <img alt="test" src="https://github.com/whitemech/logaut/workflows/test/badge.svg">
  </a>
  <a href="">
    <img alt="lint" src="https://github.com/whitemech/logaut/workflows/lint/badge.svg">
  </a>
  <a href="">
    <img alt="docs" src="https://github.com/whitemech/logaut/workflows/docs/badge.svg">
  </a>
  <a href="https://codecov.io/gh/marcofavorito/logaut">
    <img alt="codecov" src="https://codecov.io/gh/marcofavorito/logaut/branch/master/graph/badge.svg?token=FG3ATGP5P5">
  </a>
</p>
<p align="center">
  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">
    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">
  </a>
  <a href="https://img.shields.io/badge/mypy-checked-blue">
    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">
  </a>
  <a href="https://img.shields.io/badge/code%20style-black-black">
    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />
  </a>
  <a href="https://www.mkdocs.org/">
    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">
  </a>
</p>


LOGics formalisms to AUTomata

## What is `logaut`

Logaut is to the logics-to-DFA problem
what Keras is for Deep Learning:
a wrapper to performant back-ends,
but with human-friendly APIs.

## Install

To install the package from PyPI:
```
pip install logaut
```

Make sure to have [Lydia](https://github.com/whitemech/lydia) 
installed on your machine.
We suggest the following setup:

- [Install Docker](https://www.docker.com/get-started)
- Download the Lydia Docker image:
```
docker pull whitemech/lydia:latest
```
- Make the Docker image executable under the name `lydia`.
  On Linux and MacOS machines, the following commands should work:
```
echo '#!/usr/bin/env sh' > lydia
echo 'docker run -v$(pwd):/home/default whitemech/lydia lydia $@' >> lydia
sudo chmod u+x lydia
sudo mv lydia /usr/local/bin/
```

This will install an alias to the inline Docker image execution
in your system PATH. Instead of `/usr/local/bin/`
you may use another path which is still in the `PATH` variable.

## Quickstart

Now you are ready to go:
```python
from logaut import ltl2dfa
from pylogics.parsers import parse_ltl
formula = parse_ltl("F(a)")
dfa = ltl2dfa(formula, backend="lydia")
```

The function `ltl2dfa` takes in input a 
[pylogics](https://github.com/whitemech/pylogics) 
`formula` and gives in output
a [pythomata](https://github.com/whitemech/pythomata) DFA.

Then, you can manipulate the DFA as done with Pythomata,
e.g. to print:
```
dfa.to_graphviz().render("eventually.dfa")
```

Currently, the `lydia` backend only supports
the `ltl` and `ldl` logics.

The `ltlf2dfa`, based on 
[LTLf2DFA](https://github.com/whitemech/LTLf2DFA/),
supports `ltl` and `pltl`.
First, install it at version `1.0.1`:
```
pip install git+https://github.com/whitemech/LTLf2DFA.git@develop#egg=ltlf2dfa
```

Then, you can use:
```python
from logaut import pltl2dfa
from pylogics.parsers import parse_pltl
formula = parse_pltl("a S b")
dfa = pltl2dfa(formula, backend="ltlf2dfa")
```

## Write your own backend

You can write your back-end by implementing
the `Backend` interface:

```python
from logaut.backends.base import Backend

class MyBackend(Backend):

    def ltl2dfa(self, formula: Formula) -> DFA:
        """From LTL to DFA."""

    def ldl2dfa(self, formula: Formula) -> DFA:
        """From LDL to DFA."""

    def pltl2dfa(self, formula: Formula) -> DFA:
        """From PLTL to DFA."""

    def pldl2dfa(self, formula: Formula) -> DFA:
        """From PLDL to DFA."""
        
    def fol2dfa(self, formula: Formula) -> DFA:
        """From FOL to DFA."""

    def mso2dfa(self, formula: Formula) -> DFA:
        """From MSO to DFA."""
```

Then, you can register the custom backend
class in the library:

```python
from logaut.backends import register
register(id_="my_backend", entry_point="dotted.path.to.MyBackend")
```

And then, use it through the main entry point:
```python
dfa = ltl2dfa(formula, backend="my_backend")
```

## Tests

To run tests: `tox`

To run only the code tests: `tox -e py3.7`

To run only the linters: 
- `tox -e flake8`
- `tox -e mypy`
- `tox -e black-check`
- `tox -e isort-check`

Please look at the `tox.ini` file for the full list of supported commands. 

## Docs

To build the docs: `mkdocs build`

To view documentation in a browser: `mkdocs serve`
and then go to [http://localhost:8000](http://localhost:8000)

## License

logaut is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).

Copyright 2021 WhiteMech

## Authors

- [Marco Favorito](https://marcofavorito.me/)
