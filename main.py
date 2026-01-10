"""
Oldham Quiz - A multi-player quiz game with buzzer support.

This module implements a quiz game that supports both single-player and
multi-player modes with buzzer functionality for competitive play.
"""

import json
import sys
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class Colours:
    """ANSI color codes for terminal output."""
    # Basic Colours
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Reset
    RESET = '\033[0m'

    @staticmethod
    def disable():
        """Disable Colours (for non-ANSI terminals)."""
        Colours.RED = ''
        Colours.GREEN = ''
        Colours.YELLOW = ''
        Colours.BLUE = ''
        Colours.MAGENTA = ''
        Colours.CYAN = ''
        Colours.WHITE = ''
        Colours.BOLD = ''
        Colours.UNDERLINE = ''
        Colours.RESET = ''


class HighScoreDatabase:
    """Manages high scores using SQLite database."""

    def __init__(self, db_path: str = 'high_scores.db'):
        """
        Initialize the high score database.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create the high scores table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                game_mode TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_score(self, player_name: str, score: int, total_questions: int,
                  game_mode: str):
        """
        Add a new high score to the database.

        Args:
            player_name: Name of the player
            score: Number of correct answers
            total_questions: Total number of questions
            game_mode: 'single' or 'multiplayer'
        """
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO high_scores (player_name, score, total_questions, percentage, game_mode, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_name, score, total_questions, percentage, game_mode, timestamp))
        conn.commit()
        conn.close()

    def get_top_scores(self, limit: int = 10, game_mode: Optional[str] = None) -> List[Dict]:
        """
        Get the top high scores.

        Args:
            limit: Maximum number of scores to return
            game_mode: Filter by game mode ('single', 'multiplayer', or None for all)

        Returns:
            List of score dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if game_mode:
            cursor.execute('''
                SELECT player_name, score, total_questions, percentage, game_mode, timestamp
                FROM high_scores
                WHERE game_mode = ?
                ORDER BY percentage DESC, score DESC, timestamp ASC
                LIMIT ?
            ''', (game_mode, limit))
        else:
            cursor.execute('''
                SELECT player_name, score, total_questions, percentage, game_mode, timestamp
                FROM high_scores
                ORDER BY percentage DESC, score DESC, timestamp ASC
                LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'player_name': row[0],
                'score': row[1],
                'total_questions': row[2],
                'percentage': row[3],
                'game_mode': row[4],
                'timestamp': row[5]
            }
            for row in rows
        ]

    def display_leaderboard(self, limit: int = 10, game_mode: Optional[str] = None):
        """
        Display the high scores leaderboard.

        Args:
            limit: Maximum number of scores to display
            game_mode: Filter by game mode
        """
        scores = self.get_top_scores(limit, game_mode)

        if not scores:
            print(f"\n{Colours.YELLOW}No high scores yet. Be the first!{Colours.RESET}\n")
            return

        mode_text = f" ({game_mode.upper()})" if game_mode else " (ALL MODES)"
        print("\n" + "=" * 70)
        print(f"{Colours.BOLD}{Colours.MAGENTA}HIGH SCORES LEADERBOARD{mode_text}{Colours.RESET}")
        print("=" * 70)

        for rank, score_data in enumerate(scores, 1):
            mode_badge = "[S]" if score_data['game_mode'] == 'single' else "[M]"
            timestamp = score_data['timestamp'].split()[0]  # Just the date

            print(f"{Colours.CYAN}{rank:2d}. {score_data['player_name']:<20}{Colours.RESET} "
                  f"{Colours.BOLD}{score_data['score']:2d}/{score_data['total_questions']:2d}{Colours.RESET} "
                  f"({score_data['percentage']:5.1f}%)  "
                  f"{Colours.YELLOW}{mode_badge}{Colours.RESET}  "
                  f"{Colours.WHITE}{timestamp}{Colours.RESET}")

        print("=" * 70)
        print(f"{Colours.WHITE}Legend: [S] = Single Player, [M] = Multiplayer{Colours.RESET}\n")


# Platform-specific key press detection
if sys.platform.startswith('win'):
    import msvcrt
else:
    import tty
    import termios


class Player:
    """Represents a quiz player with name and score."""

    def __init__(self, name: str, key: str = None):
        """
        Initialize a player.

        Args:
            name: Player's display name
            key: Buzzer key assigned to player (for multiplayer mode)
        """
        self.name = name
        self.key = key
        self.score = 0

    def add_point(self):
        """Add one point to the player's score."""
        self.score += 1

    def __repr__(self):
        return f"Player(name={self.name}, score={self.score}, key={self.key})"


class Question:
    """Represents a quiz question with multiple choice options."""

    def __init__(self, data: dict):
        """
        Initialize a question from JSON data.

        Args:
            data: Dictionary containing question data
        """
        self.index = data['question_index']
        self.text = data['question']
        self.options = data['options']
        self.answer = data['answer']

    def display(self):
        """Display the question and its options."""
        print(f"\n{Colours.CYAN}{Colours.BOLD}Question {self.index}:{Colours.RESET} {Colours.WHITE}{self.text}{Colours.RESET}")
        for option in self.options:
            print(f"  {Colours.YELLOW}{option}{Colours.RESET}")


class BuzzerInput:
    """Handles buzzer input detection across different platforms."""

    VALID_KEYS = ('Q', 'P', 'B')

    def __init__(self):
        """Initialize buzzer input handler."""
        self.is_tty = os.isatty(sys.stdin.fileno())

    def wait_for_buzz(self) -> str:
        """
        Wait for a valid buzzer key press.

        Returns:
            The pressed key (Q, P, or B)
        """
        if sys.platform.startswith('win'):
            return self._wait_for_buzz_windows()
        else:
            return self._wait_for_buzz_unix()

    def _wait_for_buzz_windows(self) -> str:
        """Wait for buzzer key on Windows."""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').upper()
                if key in self.VALID_KEYS:
                    return key

    def _wait_for_buzz_unix(self) -> str:
        """Wait for buzzer key on Unix-like systems."""
        if not self.is_tty:
            # Fallback for IDE/non-TTY environments
            return self._wait_for_buzz_fallback()

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                key = sys.stdin.read(1).upper()
                if key in self.VALID_KEYS:
                    return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _wait_for_buzz_fallback(self) -> str:
        """Fallback input method for non-TTY environments."""
        while True:
            key = input("").upper().strip()
            if key in self.VALID_KEYS:
                return key
            print(f"{Colours.RED}Invalid key! Please enter {', '.join(self.VALID_KEYS)}.{Colours.RESET}")

    @staticmethod
    def get_valid_answer() -> str:
        """
        Get a valid answer (A, B, or C) from the user.

        Returns:
            The user's answer choice
        """
        while True:
            user_answer = input("Answer >> ").upper().strip()
            if user_answer in ('A', 'B', 'C'):
                return user_answer
            else:
                print(f"{Colours.RED}Invalid input! Please enter A, B, or C.{Colours.RESET}")


class QuizGame(ABC):
    """Abstract base class for quiz game modes."""

    def __init__(self, questions: List[Question], num_players: int,
                 high_score_db: HighScoreDatabase):
        """
        Initialize the quiz game.

        Args:
            questions: List of Question objects
            num_players: Number of players in the game
            high_score_db: High score database instance
        """
        self.questions = questions
        self.num_players = num_players
        self.players: Dict[str, Player] = {}
        self.high_score_db = high_score_db

    @abstractmethod
    def setup_players(self):
        """Set up players for the game mode."""
        pass

    @abstractmethod
    def play_question(self, question: Question, question_num: int) -> bool:
        """
        Play a single question.

        Args:
            question: The question to play
            question_num: Current question number (0-indexed)

        Returns:
            True if question was answered, False otherwise
        """
        pass

    def display_final_results(self):
        """Display final game results."""
        print("\n" + "=" * 50)
        print(f"{Colours.BOLD}{Colours.MAGENTA}FINAL RESULTS{Colours.RESET}")
        print("=" * 50)

        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.score,
            reverse=True
        )

        # Save scores to database
        game_mode = self.get_game_mode()
        for player in sorted_players:
            self.high_score_db.add_score(
                player.name,
                player.score,
                len(self.questions),
                game_mode
            )

        for rank, player in enumerate(sorted_players, 1):
            percentage = (player.score / len(self.questions)) * 100
            print(f"{Colours.CYAN}{rank}. {player.name}:{Colours.RESET} {Colours.BOLD}{player.score}/"
                  f"{len(self.questions)}{Colours.RESET} ({percentage:.1f}%)")

        self._display_winner(sorted_players)
        print("=" * 50)

    @abstractmethod
    def get_game_mode(self) -> str:
        """Return the game mode identifier ('single' or 'multiplayer')."""
        pass

    @abstractmethod
    def _display_winner(self, sorted_players: List[Player]):
        """Display the winner(s)."""
        pass

    def run(self):
        """Run the complete quiz game."""
        self.setup_players()

        for i, question in enumerate(self.questions):
            question.display()
            self.play_question(question, i)

        self.display_final_results()


class SinglePlayerGame(QuizGame):
    """Single player quiz game mode."""

    def setup_players(self):
        """Set up the single player."""
        name = input("Player name: ").strip()
        if not name:
            name = "Player 1"
        self.players['Q'] = Player(name, 'Q')

    def play_question(self, question: Question, question_num: int) -> bool:
        """Play a question in single player mode."""
        player = self.players['Q']
        user_answer = BuzzerInput.get_valid_answer()

        if user_answer == question.answer:
            player.add_point()
            print(f"{Colours.GREEN}Correct! +1 point.{Colours.RESET} Score: {Colours.BOLD}{player.score}/{question_num + 1}{Colours.RESET}")
        else:
            print(f"{Colours.RED}Incorrect.{Colours.RESET} The correct answer was {Colours.BOLD}{question.answer}{Colours.RESET}. "
                  f"Score: {Colours.BOLD}{player.score}/{question_num + 1}{Colours.RESET}")

        return True

    def _display_winner(self, sorted_players: List[Player]):
        """Display single player results."""
        pass  # No winner announcement in single player

    def get_game_mode(self) -> str:
        """Return the game mode identifier."""
        return 'single'


class MultiPlayerGame(QuizGame):
    """Multi-player quiz game mode with buzzer support."""

    MAX_ATTEMPTS = 2
    BUZZER_KEYS = ('Q', 'P', 'B')

    def __init__(self, questions: List[Question], num_players: int,
                 high_score_db: HighScoreDatabase):
        """Initialize multiplayer game."""
        super().__init__(questions, num_players, high_score_db)
        self.buzzer = BuzzerInput()

    def setup_players(self):
        """Set up multiple players."""
        for i in range(self.num_players):
            key = self.BUZZER_KEYS[i]
            name = input(f"Player {i + 1} (Key: {key}): ").strip()
            if not name:
                name = f"Player {i + 1}"
            self.players[key] = Player(name, key)

        self._display_buzzer_info()

    def _display_buzzer_info(self):
        """Display buzzer key assignments and setup info."""
        print("\n" + "=" * 50)
        print(f"{Colours.BOLD}{Colours.BLUE}BUZZER KEYS:{Colours.RESET}")
        for player in self.players.values():
            print(f"  {Colours.YELLOW}{player.key}{Colours.RESET} - {Colours.CYAN}{player.name}{Colours.RESET}")
        print("=" * 50 + "\n")

        if not self.buzzer.is_tty:
            print("It looks like you're running in an IDE console.")
            print("No worries! On buzz in, you will have to press "
                  "enter after your key.")
            print("To have the buzzer more realistic, run the game with "
                  "`python3 main.py` in a terminal.")
            input("Press enter to confirm you have read the above...")

    def play_question(self, question: Question, question_num: int) -> bool:
        """Play a question in multiplayer mode."""
        attempts = 0
        first_buzzer = None

        while attempts < self.MAX_ATTEMPTS:
            print(f"\n{Colours.BOLD}{Colours.MAGENTA}BUZZ IN WITH YOUR KEY{Colours.RESET}")
            buzzer_key = self.buzzer.wait_for_buzz()

            if not self._is_valid_buzz(buzzer_key, first_buzzer, attempts):
                continue

            player = self.players[buzzer_key]
            print(f"{Colours.CYAN}{player.name}{Colours.RESET} buzzed in.")

            if attempts == 0:
                first_buzzer = buzzer_key

            user_answer = BuzzerInput.get_valid_answer()
            attempts += 1

            if user_answer == question.answer:
                player.add_point()
                if attempts == 1:
                    print(f"{Colours.GREEN}Correct. +1 point to {player.name}{Colours.RESET}")
                else:
                    print(f"{Colours.GREEN}Correct! Steal successful. +1 point to {player.name}{Colours.RESET}")
                break
            else:
                if attempts == 1:
                    print(f"{Colours.RED}Incorrect.{Colours.RESET} Steal opportunity available.")
                else:
                    print(f"{Colours.RED}Incorrect.{Colours.RESET} The correct answer was {Colours.BOLD}{question.answer}{Colours.RESET}")
                    print("Question skipped.")
                    break

        self._display_current_scores()

        if question_num < len(self.questions) - 1:
            input("\nPress Enter for next question...")

        return True

    def _is_valid_buzz(self, buzzer_key: str, first_buzzer: Optional[str],
                       attempts: int) -> bool:
        """
        Check if a buzz is valid.

        Args:
            buzzer_key: The key that was pressed
            first_buzzer: The first player to buzz (if any)
            attempts: Number of attempts so far

        Returns:
            True if the buzz is valid, False otherwise
        """
        if buzzer_key not in self.players:
            print(f"\n{Colours.RED}Key {buzzer_key} is not assigned to a player.{Colours.RESET}")
            return False

        if attempts == 1 and buzzer_key == first_buzzer:
            print(f"{Colours.RED}{self.players[buzzer_key].name} already attempted "
                  f"this question.{Colours.RESET}")
            return False

        return True

    def _display_current_scores(self):
        """Display current scores for all players."""
        print("\n" + "-" * 50)
        print(f"{Colours.BOLD}{Colours.BLUE}CURRENT SCORES:{Colours.RESET}")
        for player in sorted(self.players.values(), key=lambda p: p.key):
            print(f"  {Colours.CYAN}{player.name}:{Colours.RESET} {Colours.BOLD}{player.score}{Colours.RESET}")
        print("-" * 50)

    def _display_winner(self, sorted_players: List[Player]):
        """Display the game winner."""
        if sorted_players:
            winner = sorted_players[0]
            print(f"\n{Colours.GREEN}{Colours.BOLD}Winner: {winner.name} with {winner.score} points!{Colours.RESET}")

    def get_game_mode(self) -> str:
        """Return the game mode identifier."""
        return 'multiplayer'


def load_questions(filepath: str) -> List[Question]:
    """
    Load questions from a JSON file.

    Args:
        filepath: Path to the questions JSON file

    Returns:
        List of Question objects
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Question(q) for q in data]


def show_warranty():
    """Display warranty information."""
    print("""
THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
""")


def show_conditions():
    """Display redistribution conditions."""
    print("""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
""")


def main():
    """Main entry point for the quiz game."""
    questions = load_questions('questions.json')
    high_score_db = HighScoreDatabase()

    print(f"\n{Colours.BOLD}{Colours.CYAN}=== OLDHAM QUIZ ==={Colours.RESET}")
    print(f"{Colours.WHITE}Copyright (C) 2026 DecBr1{Colours.RESET}")
    print("This program comes with ABSOLUTELY NO WARRANTY; for details type 'w'.")
    print("This is free software, and you are welcome to redistribute it under certain conditions; for details type 'c'.\n")
    response = input("Press Enter to continue, or type 'w' or 'c': ").strip().lower()
    if response == 'w':
        show_warranty()
        input("\nPress Enter to continue...")
    elif response == 'c':
        show_conditions()
        input("\nPress Enter to continue...")

    # Main menu loop
    while True:
        print()
        print(f"{Colours.BOLD}{Colours.CYAN}MAIN MENU{Colours.RESET}")
        print(f"1. {Colours.GREEN}Start New Game{Colours.RESET}")
        print(f"2. {Colours.YELLOW}View High Scores{Colours.RESET}")
        print(f"3. {Colours.RED}Exit{Colours.RESET}")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '2':
            # View high scores
            print()
            print(f"1. {Colours.CYAN}All Scores{Colours.RESET}")
            print(f"2. {Colours.CYAN}Single Player Only{Colours.RESET}")
            print(f"3. {Colours.CYAN}Multiplayer Only{Colours.RESET}")
            print(f"4. {Colours.CYAN}Back to Main Menu{Colours.RESET}")

            view_choice = input("\nSelect option (1-4): ").strip()

            if view_choice == '1':
                high_score_db.display_leaderboard()
                input("Press Enter to continue...")
            elif view_choice == '2':
                high_score_db.display_leaderboard(game_mode='single')
                input("Press Enter to continue...")
            elif view_choice == '3':
                high_score_db.display_leaderboard(game_mode='multiplayer')
                input("Press Enter to continue...")
            continue

        elif choice == '3':
            print(f"\n{Colours.CYAN}Thanks for playing!{Colours.RESET}\n")
            break

        elif choice == '1':
            # Start game
            print()
            num_players = 0
            while num_players < 1 or num_players > 3:
                try:
                    num_players = int(input("How many players? (1-3): "))
                    if num_players < 1 or num_players > 3:
                        print(f"{Colours.RED}Please enter a number between 1 and 3.{Colours.RESET}")
                except ValueError:
                    print(f"{Colours.RED}Please enter a valid number.{Colours.RESET}")

            print()  # Add blank line for spacing

            if num_players == 1:
                game = SinglePlayerGame(questions, num_players, high_score_db)
            else:
                game = MultiPlayerGame(questions, num_players, high_score_db)

            game.run()

            # Ask if they want to see high scores after game
            print()
            view_scores = input(f"{Colours.YELLOW}View high scores? (y/n): {Colours.RESET}").strip().lower()
            if view_scores == 'y':
                high_score_db.display_leaderboard()
                input("\nPress Enter to continue...")
        else:
            print(f"{Colours.RED}Invalid option. Please select 1, 2, or 3.{Colours.RESET}")



if __name__ == "__main__":
    main()
