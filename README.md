# ESP-Oldham-Quiz

A terminal-based quiz game about Oldham Athletic Football Club, created as practice for DSD ESP Task 4a. This project features both **Python** and **Go** implementations with full feature parity.

## Project Overview

This repository contains a multi-language quiz application with:
- **Python Implementation**: Original version written without generative AI (located in `python/src/`)
- **Go Implementation**: Conversion written with AI assistance to practice Go (located in `golang/`)
- **Shared Resources**: Both implementations use the same `questions.json` and `high_scores.db` files

## Features

- **Single Player Mode**: Answer questions solo and try to beat your high score
- **Multiplayer Mode**: Competitive gameplay with real-time buzzer system
- **High Score Database**: Persistent SQLite database tracks all scores across both implementations
- **Pandas DataFrame Integration**: View and sort high scores using pandas DataFrames
- **Matplotlib Charts**: Visualise scores with bar and pie charts (Python only)
- **Colourised Output**: ANSI colour-coded terminal UI for enhanced readability
- **Modular Questions**: JSON-based question format
- **Real-time Buzzer System**: Quick-response gameplay without needing to hit Enter
- **Cross-Platform Support**: Everything, even buzzer input, works on Linux, macOS, and Windows
- **PyInstaller Support**: Build standalone executables (Python only)
- **GPL Licensed**: Free and open-source software

## Repository Structure

```
ESP-Oldham-Quiz/
├── README.md               # This file - project overview
├── LICENSE                 # GNU GPL v3 License
├── questions.json          # Quiz questions (shared by both implementations)
├── high_scores.db          # SQLite database (auto-created, shared by both)
│
├── python/                 # Python Implementation
│   ├── README.md           # Python-specific documentation
│   ├── src/
│   │   ├── main.py         # Entry point - game loop and menu
│   │   └── oldham_quiz/    # Main package
│   │       ├── __init__.py         # Package initialization
│   │       ├── colours.py          # ANSI colour codes
│   │       ├── database.py         # High score database manager (SQLite)
│   │       ├── dataframe.py        # Pandas DataFrame functionality
│   │       ├── charts.py           # Matplotlib bar and pie charts
│   │       ├── display_strategies.py  # Display formatting functions
│   │       ├── models.py           # Player and Question data models
│   │       ├── input_handler.py    # Buzzer/keyboard input handling
│   │       ├── game_modes.py       # Game mode implementations
│   │       ├── logger.py           # Logging utilities
│   │       └── utils.py            # Helper functions (inc. PyInstaller support)
│   └── old/                # Archived backup files
│       ├── old_main_bkp.py
│       ├── single_player_bkp.py
│       ├── dataframe_reference_usage.py
│       └── test_highscores.py
│
└── golang/                 # Go Implementation
    ├── README.md           # Go-specific documentation
    ├── go.mod              # Go module definition
    ├── go.sum              # Go dependency checksums
    ├── cmd/
    │   └── main.go         # Main entry point
    └── internal/           # Internal packages
        ├── colours/
        │   └── colours.go      # ANSI color handling
        ├── database/
        │   └── database.go     # SQLite high score database
        ├── game/
        │   └── game.go         # Game modes implementation
        ├── input/
        │   └── input.go        # Input handling for buzzer
        ├── models/
        │   └── models.go       # Player and Question models
        └── utils/
            └── utils.go        # Utility functions
```

## Module Correspondence

Both implementations follow the same architecture with language-specific adaptations:

| Python Module | Go Package | Purpose |
|---------------|------------|---------|
| `main.py` | `cmd/main.go` | Entry point, main menu, game loop |
| `colours.py` | `internal/colours/colours.go` | ANSI colour codes and terminal styling |
| `models.py` | `internal/models/models.go` | Player and Question data structures |
| `database.py` | `internal/database/database.go` | SQLite high score persistence |
| `dataframe.py` | *(Python-specific)* | Pandas DataFrame wrapper for analysis |
| `charts.py` | *(Python-specific)* | Matplotlib visualisations (bar/pie charts) |
| `display_strategies.py` | *(Python-specific)* | Pluggable display formatting functions |
| `input_handler.py` | `internal/input/input.go` | Cross-platform keyboard input |
| `game_modes.py` | `internal/game/game.go` | Single/multiplayer game logic |
| `logger.py` | *(Python-specific)* | Logging utilities |
| `utils.py` | `internal/utils/utils.go` | Question loading, warranties, helpers |

## Download and Run

### Python Version

**Requirements:**
- Python 3.7 or higher
- External dependencies:
  - `pandas` - DataFrame functionality and high score analysis
  - `matplotlib` - Chart visualisations

**Install dependencies:**
```bash
pip install pandas matplotlib
```

**Running:**
```bash
cd python/src
python3 main.py
```

### Go Version

**Requirements:**
- Go 1.16 or higher
- Dependencies: `github.com/mattn/go-sqlite3`

**Building and Running:**
```bash
cd golang
go mod download          # Install dependencies
go build -o oldham-quiz ./cmd/main.go
./oldham-quiz
```

**Or run directly:**
```bash
cd golang
go run cmd/main.go
```

## How to Play

### Starting the Game

1. **Startup Screen**: Shows GPL copyright notice
   - Press **Enter** to continue
   - Type **`w`** for warranty details
   - Type **`c`** for redistribution conditions

2. **Main Menu** (Python):
   - `1` - Start New Game
   - `2` - View High Scores (SQLite Database)
   - `3` - View High Scores (Pandas DataFrame)
   - `4` - View a Matplotlib Chart
   - `5` - Exit

### Single Player Mode

1. Select `1` player when prompted
2. Enter your name
3. Answer each question by typing A, B, or C
4. Your score is automatically saved to the database

### Multiplayer Mode (2-3 Players)

1. Select `2` or `3` players
2. Each player enters their name and receives a buzzer key:
   - **Player 1**: Q key
   - **Player 2**: P key
   - **Player 3**: B key
3. Press your buzzer key first to answer
4. Type your answer (A, B, or C)
5. On incorrect answer, another player can steal the point
6. Winner announced at the end with all scores saved

### Gameplay Rules

- **First to Buzz**: Fastest player gets first attempt
- **One Steal Opportunity**: If wrong, one other player can attempt
- **1 Point per Question**: Correct answers award 1 point
- **No Repeat Attempts**: Can't buzz twice on same question

## High Scores & Leaderboard

Both implementations share the same SQLite database (`high_scores.db`):

- **Automatic Saving**: All scores saved after each game
- **Persistent Storage**: Scores survive restarts and work across both implementations
- **Filtered Views**: View all scores, single-player only, or multiplayer only
- **Top 10 Rankings**: Sorted by percentage, then score, then date
- **Mode Indicators**: `[S]` for Single Player, `[M]` for Multiplayer

### Python-Specific Features

- **Pandas DataFrame View**: Sort by score or alphabetically by name
- **Matplotlib Charts**: Visualise scores with bar or pie charts

## Architecture & Design

### Code Architecture

Both implementations use modular, object-oriented design:

**Python:**
- Object-oriented with classes and inheritance
- `QuizGame` abstract base class → `SinglePlayerGame`, `MultiPlayerGame`
- **Strategy Pattern**: Pluggable display functions (`simple_display`, `dataframe_display`)
- **Composition Over Inheritance**: `HighScoreDataframe` wraps `HighScoreDatabase`
- **Functional Approach**: Display strategies use functions instead of classes where appropriate
- Type hints throughout for clarity
- PEP 8 compliant formatting

**Go:**
- Struct-based with interface patterns
- Go interfaces for polymorphism
- Explicit error handling (no exceptions)
- Internal packages for encapsulation

### Key Design Patterns

1. **Template Method Pattern**: Base game logic with specialized implementations
2. **Strategy Pattern (Python)**: Pluggable display formatting functions without code duplication
3. **Composition Over Inheritance (Python)**: DataFrames compose databases instead of extending
4. **Single Responsibility**: Each module has one clear purpose
5. **Separation of Concerns**: UI, logic, data, and input handled separately
6. **Cross-Platform Compatibility**: Platform detection and fallback modes

### Colour Scheme

Both implementations use consistent ANSI colour coding:

- **Green**: Correct answers, winners
- **Red**: Incorrect answers, errors
- **Yellow**: Question options (A/B/C), buzzer keys
- **Cyan**: Questions, player names, rankings
- **Magenta**: Major section headers
- **Blue**: Subsection headers
- **Bold**: Emphasis on scores and titles

## Question Format

Questions are stored in `questions.json` at the repository root:

```json
{
    "question_index": 1,
    "question": "In which year was Oldham Athletic Football Club founded?",
    "options": [
        "<A> 1895",
        "<B> 1899",
        "<C> 1907"
    ],
    "answer": "A"
}
```

**Adding Questions:**
1. Open `questions.json`
2. Add a new object following the format above
3. Increment `question_index`
4. Both Python and Go versions will automatically use the new questions

## Platform Support

### Linux
-  Real-time buzzer input in terminal
-  Uses `termios`/`tty` (Python) and terminal modes (Go)
-  Full colour support

### macOS
-  Real-time buzzer input in terminal
-  Uses same Unix-based input as Linux
-  Full colour support

### Windows
-  Real-time buzzer input works natively
-  Uses `msvcrt` (Python) and Windows console API (Go)
-  Full colour support on Windows 10+

### IDE Consoles
- Fallback mode (requires Enter after key press)
- Still fully functional, slightly less responsive

## Development Notes

### Python Version
- **No AI Used**: Original implementation written manually
- **External Dependencies**: Requires `pandas` and `matplotlib`
- **PyInstaller Support**: Can be built as standalone executable using `get_resource_path()` helper
- **Modular Design**: Strategy pattern with functional composition
- **ESP Task Compliant**: Valid for marking

### Go Version
- **AI Assisted**: Written with generative AI for learning purposes
- **External Dependency**: Uses `go-sqlite3` driver
- **Not for Marking**: Practice implementation only

### Language-Specific Differences

| Feature | Python | Go |
|---------|--------|-----|
| Error Handling | Exceptions (`try/except`) | Error returns (`if err != nil`) |
| Type System | Dynamic with hints | Static with interfaces |
| Inheritance | Class-based | Interface-based composition |
| Package Privacy | Convention (`_private`) | Capitalization (exported/unexported) |
| Charts | Matplotlib (bar/pie) | Not implemented |
| DataFrames | Pandas integration | Not implemented |

## License

GNU General Public License v3 (GPL-3.0)<br>
See the [LICENSE](LICENSE) file for details.

## Additional Documentation

For implementation-specific details, see:
- [Python README](python/README.md) - Detailed Python documentation
- [Go README](golang/README.md) - Detailed Go documentation


---
