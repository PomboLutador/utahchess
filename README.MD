# Utahchess Chess Engine

## Installation Guide
- Python version: `3.8`
- Install all packages in `requirements.txt`

## Start GUI
Run file `gui/pygame/pygame_gui.py`

## Formatting & Type Checking
Formatting is kept with `isort (v5.9.3)` and `black (v21.9b0)` using the command `isort . && black .`.
Static type checking is done with `mypy (v0.910)` (with command `mypy -p utahchess` or `mypy .` from project root).
Linting is done with `flake8 (v4.0.1)` with command `flake8 --extend-ignore=F541,E203 --max-line-length=88`.

## Tests
pyTest is used for the test suite. Execute `pytest` from project root.
