# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project summary
This is a small Python package that implements a **Dots and Boxes** board state representation intended to be ML/AI-friendly (edges stored as flat 0/1 vectors).

## Common commands
### Setup (editable install)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

### Build distributions (sdist/wheel)
This repo is configured as a standard PEP 517 package via `pyproject.toml` (setuptools backend).
```bash
python -m pip install -U build
python -m build
```

### Run the example
```bash
python examples/basic_usage.py
```

### Run tests (unittest)
Run the full test suite:
```bash
python -m unittest -v
```

Run a single test module:
```bash
python -m unittest -v tests.test_board
```

Run a single test case or test method:
```bash
python -m unittest -v tests.test_board.TestBoard
python -m unittest -v tests.test_board.TestBoard.test_complete_single_box
```

### Lint/format
No linter/formatter configuration is currently checked into the repo.

## Code architecture (big picture)
### Package layout
- Source is under `src/` (set via `pyproject.toml` / setuptools configuration).
- Main public API is re-exported from `src/dots_and_boxes/__init__.py`:
  - `Board`
  - `Move`
  - `EdgeOrientation`

### Core model: `Board`
Implemented in `src/dots_and_boxes/board.py`.

Key concepts:
- The board is defined by `rows x cols` **boxes** (not dots).
- Edges are stored in two separate flat arrays for ML friendliness:
  - `horizontal_edges`: length `(rows + 1) * cols`
  - `vertical_edges`: length `rows * (cols + 1)`
- A `Move` is a single edge placement, defined in “edge coordinates”:
  - Horizontal: `(r, c)` where `r ∈ [0..rows]`, `c ∈ [0..cols-1]`
  - Vertical: `(r, c)` where `r ∈ [0..rows-1]`, `c ∈ [0..cols]`
- `IllegalMove` is raised by `Board.apply_move()` when a move is out of bounds or the edge is already set.

Important flows to know:
- **Legal move enumeration**: `Board.legal_moves()` scans both edge arrays for zeros.
- **Move application**: `Board.apply_move(move)` sets the edge and returns a list of boxes completed by that move.
  - Completion checks are localized: `boxes_completed_by_move()` only checks the (up to) 2 adjacent boxes affected by an edge.
- **AI state representation**: `Board.state_vector()` concatenates `[H..., V...]`; `Board.from_state_vector()` reconstructs a board.
- **Cloning**: `Board.copy()` makes a deep copy of the edge vectors (useful when exploring move trees).

### Tests
- `tests/test_board.py` uses the standard library `unittest` module.
- Tests cover edge counts, move legality enumeration on a small board, single-box completion behavior, and state-vector roundtrip.

## Notes
- `pyproject.toml` specifies `requires-python = ">=3.10"`.
- `src/dots_and_boxes_ai.egg-info/` is generated packaging metadata (commonly produced by editable installs) and usually should not be edited by hand.
