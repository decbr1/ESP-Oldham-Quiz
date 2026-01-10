# Oldham Quiz

A terminal-based quiz game about Oldham Athletic, created as practice for DSD ESP Task 4a.<br>
This project (and readme!) was written without use of any Generative AI.

## Features

- **Single Player Mode**: Answer questions at the pleasure of nobody but yourself.
- **Multiplayer Mode (2-3 players)**: Answer questions stressfully with friends and family.
- **High Score Database**: High Scores saved to a database, just the like arcades.
- **Colourized Output**: ANSI colours for the benefit of your eyes. And brain.
- **20 Questions**: Modular questions.json file, add your own if you so choose!
- **Real-time Buzzer System**: Buzz in quick without needing to hit enter!
- **Cross-Platform Support**: Buzzer input works on macOS, Linux, and Windows.

## Requirements

- Python 3.7 or higher
- No external dependencies required (uses standard library only)
  - `sqlite3` for database
  - `json` for question loading
  - Platform-specific modules for keyboard input (`msvcrt`, `termios`, `tty`)

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed:
   ```bash
   python3 --version
   ```

## Usage

### Running the Game

For the best experience with real-time buzzer input, run from a terminal:

```bash
python3 main.py
```

You can also run it from an IDE (PyCharm, VS Code, etc.), but buzzer input will require pressing Enter after each key in multiplayer mode.

**On Startup**: The program displays a GPL copyright notice. You can:
- Press **Enter** to continue to the game
- Type **`w`** to see warranty details
- Type **`c`** to see redistribution conditions

### Game Modes

After startup, you'll see the main menu with the following options:

1. **Start New Game** - Begin a quiz session
2. **View High Scores** - Browse the leaderboard (All, Single Player, or Multiplayer)
3. **Exit** - Quit the game

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
├── oldham_quiz/            # Main package
│   ├── __init__.py         # Package initialization and exports
│   ├── colours.py           # ANSI colour codes utility
│   ├── database.py         # High score database manager (SQLite)
│   ├── models.py           # Player and Question data models
│   ├── input_handler.py    # Buzzer and keyboard input handling
│   ├── game_modes.py       # QuizGame, SinglePlayerGame, MultiPlayerGame
│   └── utils.py            # Helper functions (load_questions, warranties)
├── main.py                 # Entry point - game loop and menu
├── questions.json          # Quiz questions database
├── high_scores.db          # SQLite database for high scores (auto-created)
├── README.md               # This file!
└── LICENSE                 # License information
```

## Code Architecture

The project uses a **modular architecture** with object-oriented programming principles. Code is organized into separate modules for maintainability:

### Modules:

**`oldham_quiz/colours.py`**
- **`Colours`**: ANSI colour codes utility class for colourised terminal output

**`oldham_quiz/database.py`**
- **`HighScoreDatabase`**: SQLite database manager for persistent high score storage

**`oldham_quiz/models.py`**
- **`Player`**: Represents a quiz player with name, key, and score
- **`Question`**: Represents a quiz question with options and answer

**`oldham_quiz/input_handler.py`**
- **`BuzzerInput`**: Handles cross-platform keyboard input

**`oldham_quiz/game_modes.py`**
- **`QuizGame`**: Abstract base class for game modes
  - **`SinglePlayerGame`**: Single-player implementation
  - **`MultiPlayerGame`**: Multiplayer implementation with buzzer logic

**`oldham_quiz/utils.py`**
- **`load_questions()`**: Load questions from JSON file
- **`show_warranty()`**: Display GPL warranty information
- **`show_conditions()`**: Display GPL redistribution conditions

**`main.py`**
- Entry point with main menu loop and game initialization

## Module Organization

```
oldham_quiz/
├── colours.py
│   └── Colours (utility class)
├── database.py
│   └── HighScoreDatabase (utility class)
├── models.py
│   ├── Player (data class)
│   └── Question (data class)
├── input_handler.py
│   └── BuzzerInput (utility class)
├── game_modes.py
│   ├── QuizGame (ABC)
│   ├── SinglePlayerGame (extends QuizGame)
│   └── MultiPlayerGame (extends QuizGame)
└── utils.py
    ├── load_questions()
    ├── show_warranty()
    └── show_conditions()
```

### Class Hierarchy

```
QuizGame (ABC)
├── SinglePlayerGame
└── MultiPlayerGame
```

## Game Flow

```
main()
  -> Load questions into Question objects
  -> Initialise HighScoreDatabase
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
      -> Option 2: View High Scores
          -> Choose filter (All/Single/Multiplayer)
          -> Display leaderboard from database
      -> Option 3: Exit
```

## **Code Quality**
- **Modular Architecture**: Code organised into separate, focused modules
- **Single Responsibility Principle**: Each module has a clear, specific purpose
- Proper docstrings for all classes and methods (Google style)
- Type hints throughout (`List[Question]`, `Optional[str]`, etc.)
- Constants in UPPER_CASE (`MAX_ATTEMPTS`, `VALID_KEYS`, `BUZZER_KEYS`)
- Consistent spacing and indentation (PEP 8 compliant)
- Line lengths kept reasonable
- Clear, descriptive variable names
- ANSI colour codes encapsulated in dedicated `Colours` utility class
- Easy to extend and maintain

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

## Colour Scheme

The game features colourised output for enhanced visual experience:

- **🟢 Green**: Correct answers, winner announcements
- **🔴 Red**: Incorrect answers, error messages, invalid input
- **🟡 Yellow**: Question options (A, B, C), buzzer keys
- **🔵 Cyan**: Question text, player names, rankings
- **🟣 Magenta**: Major section headers (BUZZ IN, FINAL RESULTS)
- **🔷 Blue**: Subsection headers (BUZZER KEYS, CURRENT SCORES)
- **Bold**: Emphasis on scores, titles, and important information

Colours work on all modern terminals using ANSI escape codes (no external dependencies required).

## High Scores & Leaderboard

The game automatically tracks all player scores in a SQLite database (`high_scores.db`).

### Features:
- **Automatic Saving**: All scores are saved automatically after each game
- **Persistent Storage**: Scores are stored permanently in SQLite database
- **Multiple Leaderboards**: View combined scores or filter by game mode
- **Top 10 Rankings**: See the best performances with percentage scores
- **Timestamp Tracking**: Each score includes the date it was achieved
- **Mode Indicators**: [S] for Single Player, [M] for Multiplayer

### Viewing High Scores:
From the main menu, select option `2` to view:
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
2. View High Scores
3. Exit

Select option (1-3): 1

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
See [LICENSE](LICENSE) file for details.

---
