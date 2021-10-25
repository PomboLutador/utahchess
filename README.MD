# Utahchess Chess Engine

## Installation Guide
- Python version: `3.8`
- Install `pygame` via `pip install pygame` (specifically `v2.0.2`) to run the GUI.
- Or use the `requirements.txt` in conjunction with a `3.8` python interpreter to mirror the entire environment.

## Start GUI
Run file `gui/pygame/pygame_gui.py`

## Formatting & Type Checking
Formatting is kept with `isort (v.5.9.3)` and `black (v21.9b0)` using the command `isort . && black .` with default settings.
Static type checking is done with `mypy (v0.910)` (with command `mypy -p utahchess` from project root).

## Tests
pyTest is used for the test suite. Execute `pytest` from project root.