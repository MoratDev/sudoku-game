# Sudoku Game

A complete Sudoku game with multiple interfaces: console, web, and desktop GUI with keyboard support.

## Features

- **4 Difficulty Levels**: Easy, Medium, Hard, Expert
- **Multiple Interfaces**: Console, Web App, Desktop GUI
- **Keyboard Support**: Full keyboard navigation and input
- **Move Validation**: Prevents invalid moves according to Sudoku rules
- **Hints System**: Get hints for specific cells
- **Solution Display**: View the complete solution anytime

## Available Versions

### 1. Console Version
```bash
python3 sudoku_game.py
```
- Text-based interface
- Simple commands: `row col number`

### 2. Web Version
```bash
python3 sudoku_web.py
```
- Opens browser automatically at `http://localhost:8000`
- Beautiful responsive web interface
- Click-based input

### 3. Desktop GUI Version (Recommended)
```bash
# Install dependencies first
python3 -m venv sudoku_env
source sudoku_env/bin/activate  # On Windows: sudoku_env\Scripts\activate
pip install -r requirements.txt

# Run the game
python3 sudoku_pygame.py
```

## Desktop GUI Controls

### Keyboard Controls (Primary)
- **Arrow Keys**: Navigate between cells
- **1-9**: Input numbers
- **Delete/Backspace/0**: Clear cell
- **N**: New game
- **H**: Get hint for selected cell
- **S**: Show complete solution

### Mouse Controls
- **Click cells**: Select cell
- **Click buttons**: New Game, Hint, Solution, etc.
- **Difficulty buttons**: Easy, Medium, Hard, Expert

## Building Executable

To create a standalone .exe file:

```bash
# Activate virtual environment
source sudoku_env/bin/activate

# Run build script
python3 build_exe.py
```

Choose option 1 (PyInstaller) for best results. The executable will be created in the `dist` folder.

## Difficulty Levels

- **Easy**: 35 empty cells (46 filled)
- **Medium**: 45 empty cells (36 filled)  
- **Hard**: 55 empty cells (26 filled)
- **Expert**: 65 empty cells (16 filled)

## Requirements

- Python 3.8+
- Pygame 2.6+ (for desktop version only)

## Testing

Run the test suite:
```bash
python3 test_sudoku.py
```

## Game Rules

Standard Sudoku rules apply:
- Fill each row with numbers 1-9
- Fill each column with numbers 1-9  
- Fill each 3x3 box with numbers 1-9
- No number can repeat in any row, column, or 3x3 box

## Files

- `sudoku_game.py` - Core game logic and console interface
- `sudoku_pygame.py` - Desktop GUI with Pygame ⭐ **Main app**
- `sudoku_web.py` - Web browser version
- `sudoku_gui.py` - Tkinter version (requires tkinter)
- `build_exe.py` - Executable builder script
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup script