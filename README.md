# Dots and Boxes (AI prototype)

This project provides a small, scalable Python board model for **Dots and Boxes**.

## Key ideas
- A board is parameterized by `rows` x `cols` *boxes* (default: 3x3).
- Edges are stored separately:
  - `horizontal_edges`: `(rows + 1) * cols`
  - `vertical_edges`: `rows * (cols + 1)`

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
python examples/basic_usage.py
```

## Running tests
```bash
python -m unittest -v
```
