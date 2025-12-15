# Dots and Boxes Game

## Overview
A Python implementation of the classic Dots and Boxes game with a web-based UI. Features a board model designed for AI training purposes.

## Project Structure
- `app.py` - Flask web server
- `templates/` - HTML templates
  - `index.html` - Game UI
- `static/` - Frontend assets
  - `css/style.css` - Styling
  - `js/game.js` - Game logic
- `src/dots_and_boxes/` - Core game library
  - `board.py` - Board class implementation
  - `__init__.py` - Package exports
- `examples/` - Usage examples
- `tests/` - Unit tests

## Running
The web server runs on port 5000:
```bash
python app.py
```

Run tests with:
```bash
python tests/test_board.py -v
```

## Game Rules
- Players take turns drawing lines between dots
- When a player completes a box (4 sides), they score a point and go again
- Player 1 is Blue, Player 2 is Red
- Game ends when all boxes are claimed

## Key Technical Concepts
- Board is parameterized by `rows` x `cols` boxes (default: 3x3)
- Edges stored separately: horizontal and vertical
- Provides state vector for AI/ML integration
