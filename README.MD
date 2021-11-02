# Utahchess Chess Engine

## Installation Guide
- Python version: `3.8`
- Install all packages in `requirements.txt`

## Start GUI
Run file `gui/pygame/pygame_gui.py`

## Formatting & Type Checking
Formatting is kept with `isort (v.5.9.3)` and `black (v21.9b0)` using the command `isort . && black .`.
Static type checking is done with `mypy (v0.910)` (with command `mypy -p utahchess` or `mypy .` from project root).

## Tests
pyTest is used for the test suite. Execute `pytest` from project root.