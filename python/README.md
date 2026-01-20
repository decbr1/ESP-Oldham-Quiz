# Oldham Quiz

A terminal-based quiz game about Oldham Athletic, created as practice for DSD ESP Task 4a.<br>
This project (and readme!) was written without use of any Generative AI.

## Features

- **Single Player Mode**: Answer questions at the pleasure of nobody but yourself.
- **Multiplayer Mode (2-3 players)**: Answer questions stressfully with friends and family.
- **High Score Database**: High Scores saved to a database, just the like arcades.
- **Pandas DataFrame Integration**: View and sort high scores with pandas DataFrames.
- **Matplotlib Charts**: Visualise your scores with bar and pie charts.
- **Colourized Output**: ANSI colours for the benefit of your eyes. And brain.
- **20 Questions**: Modular questions.json file, add your own if you so choose!
- **Real-time Buzzer System**: Buzz in quick without needing to hit enter!
- **Cross-Platform Support**: Buzzer input works on macOS, Linux, and Windows.
- **PyInstaller Support**: Build standalone executables for distribution.

## Requirements

- Python 3.7 or higher
- External dependencies:
  - `pandas` - DataFrame functionality for high score analysis
  - `matplotlib` - Chart visualisations (bar and pie charts)
- Standard library modules used:
  - `sqlite3` for database
  - `json` for question loading
  - Platform-specific modules for keyboard input (`msvcrt`, `termios`, `tty`)

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed:
   ```bash
   python3 --version
   ```
3. Install dependencies:
   ```bash
   pip install pandas matplotlib
   ```

## Usage

### Running the Game

For the best experience with real-time buzzer input, run from a terminal:

```bash
cd python/src
python3 main.py
```

You can also run it from an IDE (PyCharm, VS Code, etc.), but buzzer input will require pressing Enter after each key in multiplayer mode.

**On Startup**: The program displays a GPL copyright notice. You can:
- Press **Enter** to continue to the game
- Type **`w`** to see warranty details
- Type **`c`** to see redistribution conditions

### Main Menu

After startup, you'll see the main menu with the following options:

1. **Start New Game** - Begin a quiz session
2. **View High Scores w/ SQLite Database** - Browse the leaderboard using raw SQL
3. **View High Scores w/ Pandas DataFrame** - Browse the leaderboard using pandas (sortable)
4. **View a matplotlib chart** - Display bar or pie chart of scores
5. **Exit** - Quit the game

### Game Modes

#### Single Player
1. Select `1` when prompted for number of players
2. Enter your name
3. Answer each question by typing A, B, or C
4. See your final score at the end
5. Your score is automatically saved to the high scores database

#### Multiplayer (2-3 Players)
1. Select `2` or `3` when prompted for number of players
2. Each player enters their name and is assigned a buzzer key:
   - Player 1: **Q**
   - Player 2: **P**
   - Player 3: **B**
3. When a question appears, press your buzzer key to answer
4. Type your answer (A, B, or C)
5. If wrong, another player can steal the point
6. Winner is announced at the end
7. All scores are automatically saved to the high scores database

### Gameplay Rules (Multiplayer)

- **First to Buzz**: Press your buzzer key as fast as possible
- **Two Attempts**: If the first player is wrong, one other player can steal
- **Points**: 1 point for correct answers
- **No Repeat Attempts**: Can't buzz in twice on the same question

## Project Structure

```
ESP-Oldham-Quiz/
├── python/
│   └── src/
│       ├── main.py                 # Entry point - game loop and menu
│       └── oldham_quiz/            # Main package
│           ├── __init__.py         # Package initialization and exports
│           ├── colours.py          # ANSI colour codes utility
│           ├── database.py         # High score database manager (SQLite)
│           ├── dataframe.py        # Pandas DataFrame functionality for high scores
│           ├── charts.py           # Matplotlib bar and pie chart visualisations
│           ├── display_strategies.py  # Display formatting functions
│           ├── models.py           # Player and Question data models
│           ├── input_handler.py    # Buzzer and keyboard input handling
│           ├── game_modes.py       # QuizGame, SinglePlayerGame, MultiPlayerGame
│           ├── logger.py           # Logging utilities
│           └── utils.py            # Helper functions (load_questions, warranties, PyInstaller)
├── questions.json          # Quiz questions database
├── high_scores.db          # SQLite database for high scores (auto-created)
├── README.md               # This file!
└── LICENSE                 # License information
```

## Code Architecture

The project uses a **modular architecture** with object-oriented programming principles and functional composition. Code is organized into separate modules for maintainability:

### Modules:

**`oldham_quiz/colours.py`**
- **`Colours`**: ANSI colour codes utility class for colourised terminal output
- **`c()`**: Helper function to create coloured string instances with chainable methods

**`oldham_quiz/database.py`**
- **`HighScoreDatabase`**: SQLite database manager for persistent high score storage
  - `add_score()`: Save a player's score to the database
  - `get_top_scores()`: Retrieve top scores with optional filtering
  - `display_leaderboard()`: Display leaderboard using configurable display function (defaults to `simple_display`)

**`oldham_quiz/dataframe.py`**
- **`HighScoreDataframe`**: Pandas DataFrame wrapper for high score analysis
  - `get_dataframe()`: Returns scores as pandas DataFrame
  - `display_stats()`: Shows statistical analysis of scores
  - `display_leaderboard()`: Displays leaderboard using pandas formatting with sorting options

**`oldham_quiz/charts.py`**
- **`plot_bar()`**: Display a bar chart for score metrics using matplotlib
- **`plot_pie()`**: Display a pie chart for score distribution using matplotlib

**`oldham_quiz/display_strategies.py`**
- **`simple_display()`**: Basic text-based leaderboard formatting with ANSI colors
- **`dataframe_display()`**: Pandas-based leaderboard formatting
- **`LeaderboardDisplay`**: Type alias for display functions

**`oldham_quiz/models.py`**
- **`Player`**: Represents a quiz player with name, key, and score
- **`Question`**: Represents a quiz question with options and answer

**`oldham_quiz/input_handler.py`**
- **`BuzzerInput`**: Handles cross-platform keyboard input

**`oldham_quiz/game_modes.py`**
- **`QuizGame`**: Abstract base class for game modes
  - **`SinglePlayerGame`**: Single-player implementation
  - **`MultiPlayerGame`**: Multiplayer implementation with buzzer logic

**`oldham_quiz/logger.py`**
- Logging utilities for debug, info, warning, error, and critical messages

**`oldham_quiz/utils.py`**
- **`get_resource_path()`**: Get absolute path to resources (supports PyInstaller bundling)
- **`load_questions()`**: Load questions from JSON file
- **`show_warranty()`**: Display GPL warranty information
- **`show_conditions()`**: Display GPL redistribution conditions

**`main.py`**
- Entry point with main menu loop and game initialization

## Module Organization

```
oldham_quiz/
├── colours.py
│   ├── Colours (utility class)
│   └── c() (helper function)
├── database.py
│   └── HighScoreDatabase (utility class)
├── dataframe.py
│   └── HighScoreDataframe (wrapper class)
├── charts.py
│   ├── plot_bar() (function)
│   └── plot_pie() (function)
├── display_strategies.py
│   ├── simple_display() (function)
│   ├── dataframe_display() (function)
│   └── LeaderboardDisplay (type alias)
├── models.py
│   ├── Player (data class)
│   └── Question (data class)
├── input_handler.py
│   └── BuzzerInput (utility class)
├── game_modes.py
│   ├── QuizGame (ABC)
│   ├── SinglePlayerGame (extends QuizGame)
│   └── MultiPlayerGame (extends QuizGame)
├── logger.py
│   └── logging functions (debug, info, warning, error, critical)
└── utils.py
    ├── get_resource_path()
    ├── load_questions()
    ├── show_warranty()
    └── show_conditions()
```

### Design Patterns

**Strategy Pattern (Functional)**
- Display formatting is separated into pluggable functions
- `simple_display()` for basic text output with colors
- `dataframe_display()` for pandas-based table formatting
- Both `HighScoreDatabase` and `HighScoreDataframe` can use any display function
- Easy to extend with new formats (JSON, CSV, HTML) without modifying existing code

**Composition Over Inheritance**
- `HighScoreDataframe` wraps `HighScoreDatabase` instance
- No inheritance hierarchy between database classes
- Display logic separated from data management
- Functions over classes where state isn't needed

### Class Hierarchy

```
QuizGame (ABC)
├── SinglePlayerGame
└── MultiPlayerGame

 HighScoreDatabase (standalone)
 HighScoreDataframe (composes HighScoreDatabase)
```

## Game Flow

```
main()
  -> Load questions into Question objects
  -> Initialise HighScoreDatabase
  -> Initialise HighScoreDataframe
  -> Display copyright notice
  -> Main Menu Loop:
      -> Option 1: Start New Game
          -> Determine number of players
          -> Create SinglePlayerGame or MultiPlayerGame
          -> game.run()
              -> game.setup_players()
              -> For each question:
                  -> question.display()
                  -> game.play_question()
              -> game.display_final_results()
                  -> Save all player scores to database
          -> Prompt to view high scores
      -> Option 2: View High Scores (SQLite)
          -> Choose filter (All/Single/Multiplayer)
          -> Display leaderboard from database
      -> Option 3: View High Scores (DataFrame)
          -> Choose filter (All/Single/Multiplayer)
          -> Choose sort order (Score/Name)
          -> Display leaderboard using pandas
      -> Option 4: View Matplotlib Chart
          -> Choose chart type (Bar/Pie)
          -> Display chart with matplotlib
      -> Option 5: Exit
```

## Chart Visualisations

The game includes matplotlib-based visualisations for score data:

### Bar Chart
- Displays player scores as vertical bars
- Shows player names on x-axis, scores on y-axis
- Colour-coded bars for easy comparison

### Pie Chart
- Displays score distribution as pie segments
- Shows percentage and actual values for each player
- Handles edge case of zero total scores gracefully

## **Code Quality**
- **Modular Architecture**: Code organised into separate, focused modules
- **Single Responsibility Principle**: Each module has a clear, specific purpose
- **Functional Composition**: Display strategies use functions instead of unnecessary classes
- **Strategy Pattern**: Pluggable display formatting without code duplication
- **Composition Over Inheritance**: Dataframe wraps database instead of extending it
- Proper docstrings for all classes and methods (Google style)
- Type hints throughout (`List[Question]`, `Optional[str]`, `Callable`, etc.)
- Constants in UPPER_CASE (`MAX_ATTEMPTS`, `VALID_KEYS`, `BUZZER_KEYS`)
- Consistent spacing and indentation (PEP 8 compliant)
- Line lengths kept reasonable
- Clear, descriptive variable names
- ANSI colour codes encapsulated in dedicated `Colours` utility class
- Easy to extend and maintain
- Pythonic design - functions where classes aren't needed

## Platform Notes

### macOS/Linux
- Real-time buzzer input works in terminal
- No Enter key needed when buzzing in (in terminal mode)
- Uses `termios` and `tty` for raw keyboard input

### Windows
- Real-time buzzer input works natively
- Uses `msvcrt` for keyboard detection

### IDE Consoles
- Fallback mode activates automatically
- Requires pressing Enter after each key press
- Still fully functional, just slightly less responsive

## Building with PyInstaller

The project includes support for building standalone executables:

```bash
pip install pyinstaller
cd python/src
pyinstaller --onefile --add-data "../../questions.json:." main.py
```

The `get_resource_path()` function in `utils.py` handles finding resources whether running from source or from a PyInstaller bundle.

## Colour Scheme

The game features colourised output for enhanced visual experience:

- **Green**: Correct answers, winner announcements, start game option
- **Red**: Incorrect answers, error messages, invalid input, exit option
- **Yellow**: Question options (A, B, C), buzzer keys, high score options
- **Cyan**: Question text, player names, rankings, main menu title
- **Magenta**: Major section headers (BUZZ IN, FINAL RESULTS), chart option
- **Blue**: Subsection headers (BUZZER KEYS, CURRENT SCORES)
- **Bold**: Emphasis on scores, titles, and important information

Colours work on all modern terminals using ANSI escape codes (no external dependencies required).

## High Scores & Leaderboard

The game automatically tracks all player scores in a SQLite database (`high_scores.db`).

### Features:
- **Automatic Saving**: All scores are saved automatically after each game
- **Persistent Storage**: Scores are stored permanently in SQLite database
- **Multiple Leaderboards**: View combined scores or filter by game mode
- **Two Display Modes**: SQLite-based or Pandas DataFrame-based views
- **Sortable (DataFrame)**: Sort by score or alphabetically by player name
- **Top 10 Rankings**: See the best performances with percentage scores
- **Timestamp Tracking**: Each score includes the date it was achieved
- **Mode Indicators**: [S] for Single Player, [M] for Multiplayer

### Viewing High Scores:
From the main menu, select option `2` (SQLite) or `3` (DataFrame) to view:
1. **All Scores** - Combined leaderboard of all game modes
2. **Single Player Only** - Top single player performances
3. **Multiplayer Only** - Top multiplayer winners

After completing a game, you'll be prompted to view the leaderboard immediately.

### Database Schema:
The SQLite database stores:
- Player name
- Score (correct answers)
- Total questions
- Percentage score
- Game mode (single/multiplayer)
- Timestamp (date and time)

Scores are ranked by percentage, then by total score, then by date (earliest first).

## Example Session

```
=== OLDHAM QUIZ ===
Copyright (C) 2026 DecBr1
This program comes with ABSOLUTELY NO WARRANTY; for details type 'w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type 'c' for details.

Press Enter to continue, or type 'w' or 'c':

MAIN MENU
1. Start New Game
2. View High Scores w/ SQLite Database
3. View High Scores w/ Pandas Dataframe
4. View a matplotlib chart
5. Exit

Select option (1-5): 1

How many players? (1-3): 2

Player 1 (Key: Q): Alice
Player 2 (Key: P): Bob

==================================================
BUZZER KEYS:
  Q - Alice
  P - Bob
==================================================

Question 1: In which year was Oldham Athletic Football Club founded?
  <A> 1895
  <B> 1899
  <C> 1907

BUZZ IN WITH YOUR KEY
Alice buzzed in.
Answer >> A
Correct. +1 point to Alice

--------------------------------------------------
CURRENT SCORES:
  Alice: 1
  Bob: 0
--------------------------------------------------

Press Enter for next question...

...

==================================================
FINAL RESULTS
==================================================
1. Alice: 15/20 (75.0%)
2. Bob: 12/20 (60.0%)

Winner: Alice with 15 points!
==================================================

View high scores? (y/n): y

======================================================================
HIGH SCORES LEADERBOARD (ALL MODES)
======================================================================
 1. Charlie              20/20 (100.0%)  [S]  2026-01-10
 2. Alice                15/20 ( 75.0%)  [M]  2026-01-10
 3. Bob                  12/20 ( 60.0%)  [M]  2026-01-10
======================================================================
Legend: [S] = Single Player, [M] = Multiplayer

Press Enter to continue...
```

## Question Format

Questions in `questions.json` follow this structure:

```json
{
    "question_index": 1,
    "question": "Your question text here?",
    "options": [
        "<A> First option",
        "<B> Second option",
        "<C> Third option"
    ],
    "answer": "A"
}
```

## License

GNU General Public License v3
See [LICENSE](../LICENSE) file for details.

---
