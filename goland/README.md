# Go Implementation

This is a Go rewrite of the main oldham quiz, which can be found in `python/src/`.<br>
Unlike the main python project, generative ai **has** been used for this project. I have only written this
version of the game to better my understanding in Go; it is not valid for - and therefore should be
disregarded for - any and all marking for an ESP project.

## Project Structure

```
goland/
├── cmd/
│   └── main.go              # Main entry point
├── internal/
│   ├── colours/
│   │   └── colours.go       # ANSI color handling (converted from colours.py)
│   ├── database/
│   │   └── database.go      # SQLite high score database (converted from database.py)
│   ├── game/
│   │   └── game.go          # Game modes implementation (converted from game_modes.py)
│   ├── input/
│   │   └── input.go         # Input handling for buzzer (converted from input_handler.py)
│   ├── models/
│   │   └── models.go        # Player and Question models (converted from models.py)
│   └── utils/
│       └── utils.go         # Utility functions (converted from utils.py)
├── go.mod
└── go.sum
```

## Converted Modules

| Python Module | Go Package | Description |
|--------------|------------|-------------|
| `main.py` | `cmd/main.go` | Main entry point with menu system |
| `colours.py` | `internal/colours/colours.go` | ANSI color codes and styling |
| `models.py` | `internal/models/models.go` | Player and Question data models |
| `database.py` | `internal/database/database.go` | SQLite high score management |
| `input_handler.py` | `internal/input/input.go` | Keyboard/buzzer input handling |
| `game_modes.py` | `internal/game/game.go` | Single and multiplayer game modes |
| `utils.py` | `internal/utils/utils.go` | Question loading and info displays |

## Key Features

All features from the Python version have been preserved:

-  Single player mode
-  Multiplayer mode (up to 3 players)
-  Buzzer system with key assignments (Q, P, B)
-  High score tracking with SQLite database
-  ANSI color output for terminal UI
-  Question loading from JSON file
-  Leaderboard filtering by game mode

Furthermore, the conversion maintains functional parity with the Python implementation. <br>
^ (thats nerd speak for they use the same database)

## Building and Running

### Build the application:
```bash
cd goland
go build -o oldham-quiz ./cmd/main.go
```

### Run the application:
```bash
./oldham-quiz
```

### Or run directly:
```bash
go run cmd/main.go
```

## Dependencies

- `github.com/mattn/go-sqlite3` - SQLite driver for Go

Install dependencies:
```bash
go mod download
```

## Code Conversion Notes

### Language-Specific Changes

1. **Error Handling**: Python's exception handling converted to Go's explicit error returns
2. **Type System**: Python's dynamic types converted to Go's static types with interfaces
3. **OOP to Structs**: Python classes converted to Go structs with methods
4. **Package System**: Python's module imports converted to Go's package system

### Implementation Details

- **Colours Package**: Fluent API maintained using method chaining
- **Game Modes**: Abstract base class pattern implemented using Go interfaces
- **Input Handling**: Cross-platform terminal detection simplified for Go
- **Database**: Used `database/sql` with SQLite driver

