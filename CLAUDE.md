# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Sudoku game built with Python using Pygame and the py-sudoku library. The project consists of a single main file `pyg_sudoku.py` that implements the complete game logic and UI in a class-based architecture.

## Development Commands

### Running the Application
```bash
python pyg_sudoku.py
```

### Installing Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Building Executable
```bash
Pyinstaller -Fw -i grid.ico -n Sudoku pyg_sudoku.py
```

## Code Architecture

### Main Components

1. **SudokuGame Class**: Central game controller managing all state and behavior
   - Constants for screen dimensions, colors, and game configuration
   - Initialization methods for grid, game state, UI elements, and validation groups
   - Main game loop with event handling and rendering

2. **Grid System**:
   - 9x9 grid implemented with 81 pygame.Rect objects
   - 5px spacing between 3x3 sections for visual separation
   - Cell indexing: 0-80 (row-major order)

3. **Game State Management**:
   - `box_values`: Dictionary storing current values in each cell (0-80 keys)
   - `box_is_initial`: Dictionary tracking pre-filled cells
   - `box_has_conflict`: Dictionary tracking validation conflicts

4. **Validation System**:
   - Three validation group types: horizontal, vertical, and 3x3 sub-grids
   - Real-time conflict detection with visual feedback (red highlighting)
   - `_validate_all_cells()` method checks entire board against Sudoku rules

5. **UI Controls**:
   - Timer display showing elapsed time in MM:SS format
   - Difficulty selector (0.01-0.99) controlled by mouse wheel
   - Start button to generate new puzzles
   - Visual feedback with hover effects and color coding

6. **Game Logic**:
   - Uses `py-sudoku` library to generate puzzles with specified difficulty
   - Random seed generation for varied puzzles
   - Completion detection when all cells filled without conflicts

### Key Data Structures

- **input_boxes**: List of 81 pygame.Rect objects representing each cell
- **horizontal_groups, vertical_groups, nine_box_groups**: Lists of cell indices for validation
- **box_values, box_is_initial, box_has_conflict**: Dictionaries with 0-80 keys

### Game Flow

1. User clicks "Start" button to generate a new puzzle
2. Pre-filled cells displayed with light gray background
3. User clicks empty cells and presses number keys (1-9) to fill
4. Real-time validation highlights conflicts in red
5. Timer tracks completion time
6. Game detects completion when all cells correctly filled

### Dependencies

- **pygame>=2.6.1**: Game framework and UI rendering
- **py-sudoku>=2.0.0**: Sudoku puzzle generation and validation
- **Python>=3.13**: Minimum Python version requirement

## Development Notes

- Uses modern Python packaging with pyproject.toml
- Application runs at 60 FPS for smooth timer updates
- Mouse wheel scrolling adjusts difficulty when hovering over difficulty box
- Single main loop with comprehensive event handling
- No external assets required except for grid.ico icon for executable
- Class-based architecture with clear separation of concerns