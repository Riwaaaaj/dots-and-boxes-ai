# Dots and Boxes AI

## Overview
A Python library providing a board model for the Dots and Boxes game, designed for AI training purposes.

## Project Structure
- `src/dots_and_boxes/` - Main package source code
  - `board.py` - Board class implementation
  - `__init__.py` - Package exports
- `examples/` - Usage examples
  - `basic_usage.py` - Basic demonstration script
- `tests/` - Unit tests

## Setup
The project uses Python 3.11 with setuptools for packaging. Install with:
```bash
pip install -e .
```

## Running
Run the example with:
```bash
python examples/basic_usage.py
```

Run tests with:
```bash
python tests/test_board.py -v
```

## Key Concepts
- Board is parameterized by `rows` x `cols` boxes (default: 3x3)
- Edges stored separately: horizontal and vertical
- Provides state vector for AI/ML integration
