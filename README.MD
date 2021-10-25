# Utahchess Chess Engine

## Installation Guide
Python 3.8

## Start GUI
Run file `gui/pygame/pygame_gui.py`

## Formatting & Type Checking
Formatting is kept with `isort (v.5.9.3)` and `black (v21.9b0)` using the command `isort . && black .` with default settings.
Statis type checking is done with `mypy (v0.910)` (with command `mypy utahchess` from project root).

## Tests
pyTest is used for the test suite. Execute `pytest` from project root.