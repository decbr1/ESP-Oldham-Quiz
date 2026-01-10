# Oldham Quiz

A terminal-based quiz game about Oldham Athletic Football Club, featuring both single-player and multiplayer modes with buzzer support.

## Features

- **Single Player Mode**: Test your knowledge of Oldham Athletic on your own
- **Multiplayer Mode (2-3 players)**: Compete with friends using buzzer keys
- **Colorized Output**: Enhanced visual experience with color-coded feedback
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **20 Questions**: Comprehensive trivia about Oldham Athletic FC
- **Real-time Buzzer System**: Fast-paced competitive gameplay in multiplayer mode
- **Score Tracking**: See your progress and final results

## Requirements

- Python 3.7 or higher
- No external dependencies required (uses standard library only)

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

#### Single Player
1. Select `1` when prompted for number of players
2. Enter your name
3. Answer each question by typing A, B, or C
4. See your final score at the end

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

### Gameplay Rules (Multiplayer)

- **First to Buzz**: Press your buzzer key as fast as possible
- **Two Attempts**: If the first player is wrong, one other player can steal
- **Points**: 1 point for correct answers
- **No Repeat Attempts**: Can't buzz in twice on the same question

## Project Structure

```
ESP-Oldham-Quiz/
├── main.py              # Main game logic and classes
├── questions.json       # Quiz questions database
├── README.md            # This file!
└── LICENSE              # License information
```

## Code Architecture

The project uses object-oriented programming with the following key classes:

- **`Colors`**: ANSI color codes utility class for colorized terminal output
- **`Player`**: Represents a quiz player with name, key, and score
- **`Question`**: Represents a quiz question with options and answer
- **`BuzzerInput`**: Handles cross-platform keyboard input
- **`QuizGame`**: Abstract base class for game modes
  - **`SinglePlayerGame`**: Single-player implementation
  - **`MultiPlayerGame`**: Multiplayer implementation with buzzer logic

## Class Hierarchy

```
QuizGame (ABC)
├── SinglePlayerGame
└── MultiPlayerGame

Player (data class)
Question (data class)
BuzzerInput (utility class)
Colors (utility class)
```

## Game Flow

```
main()
  → Load questions into Question objects
  → Determine number of players
  → Create SinglePlayerGame or MultiPlayerGame
  → game.run()
      → game.setup_players()
      → For each question:
          → question.display()
          → game.play_question()
      → game.display_final_results()
```

## **PEP8 Compliance**
- Proper docstrings for all classes and methods (Google style)
- Type hints throughout (`List[Question]`, `Optional[str]`, etc.)
- Constants in UPPER_CASE (`MAX_ATTEMPTS`, `VALID_KEYS`, `BUZZER_KEYS`)
- Consistent spacing and indentation
- Line lengths kept reasonable
- Clear, descriptive variable names
- ANSI color codes encapsulated in dedicated `Colors` utility class

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

## Color Scheme

The game features colorized output for enhanced visual experience:

- **🟢 Green**: Correct answers, winner announcements
- **🔴 Red**: Incorrect answers, error messages, invalid input
- **🟡 Yellow**: Question options (A, B, C), buzzer keys
- **🔵 Cyan**: Question text, player names, rankings
- **🟣 Magenta**: Major section headers (BUZZ IN, FINAL RESULTS)
- **🔷 Blue**: Subsection headers (BUZZER KEYS, CURRENT SCORES)
- **Bold**: Emphasis on scores, titles, and important information

Colors work on all modern terminals using ANSI escape codes (no external dependencies required).

## Example Session

```
=== OLDHAM QUIZ ===
Copyright (C) 2026 DecBr1
This program comes with ABSOLUTELY NO WARRANTY; for details type 'w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type 'c' for details.

Press Enter to continue, or type 'w' or 'c': 

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
