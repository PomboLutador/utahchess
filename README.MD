# Utahchess Chess Engine

## Installation Guide
- Python version: `3.8`
- Install all packages in `requirements.txt`

## Start GUI
Run file `gui/pygame/pygame_gui.py`

## Formatting & Type Checking
Formatting is kept with `isort` and `black` using the command `isort --skip env . && black --exclude env .` 
(assuming a `virtualenv` is installed in `env`). 
`pyproject.toml` contains the settings for `isort` to be compatible with `black`.


Static type checking is done with `mypy` (with command `mypy -p utahchess` or `mypy .` from project root).


Linting is done with `flake8 (v4.0.1)` with command `flake8 --extend-ignore=F541,E203 --max-line-length=88`.

## Tests
pytest is used for the test suite. Execute `pytest` from project root.
