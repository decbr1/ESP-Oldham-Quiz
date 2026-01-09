"""
Oldham Quiz - A multi-player quiz game with buzzer support.

This module implements a quiz game that supports both single-player and
multi-player modes with buzzer functionality for competitive play.
"""

import json
import sys
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

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
        print(f"\nQuestion {self.index}: {self.text}")
        for option in self.options:
            print(f"  {option}")


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
            print(f"Invalid key! Please enter {', '.join(self.VALID_KEYS)}.")

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
                print("Invalid input! Please enter A, B, or C.")


class QuizGame(ABC):
    """Abstract base class for quiz game modes."""

    def __init__(self, questions: List[Question], num_players: int):
        """
        Initialize the quiz game.

        Args:
            questions: List of Question objects
            num_players: Number of players in the game
        """
        self.questions = questions
        self.num_players = num_players
        self.players: Dict[str, Player] = {}

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
        print("FINAL RESULTS")
        print("=" * 50)

        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.score,
            reverse=True
        )

        for rank, player in enumerate(sorted_players, 1):
            percentage = (player.score / len(self.questions)) * 100
            print(f"{rank}. {player.name}: {player.score}/"
                  f"{len(self.questions)} ({percentage:.1f}%)")

        self._display_winner(sorted_players)
        print("=" * 50)

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
            print(f"Correct! +1 point. Score: {player.score}/{question_num + 1}")
        else:
            print(f"Incorrect. The correct answer was {question.answer}. "
                  f"Score: {player.score}/{question_num + 1}")

        return True

    def _display_winner(self, sorted_players: List[Player]):
        """Display single player results."""
        pass  # No winner announcement in single player


class MultiPlayerGame(QuizGame):
    """Multi-player quiz game mode with buzzer support."""

    MAX_ATTEMPTS = 2
    BUZZER_KEYS = ('Q', 'P', 'B')

    def __init__(self, questions: List[Question], num_players: int):
        """Initialize multiplayer game."""
        super().__init__(questions, num_players)
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
        print("BUZZER KEYS:")
        for player in self.players.values():
            print(f"  {player.key} - {player.name}")
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
            print("\nBUZZ IN WITH YOUR KEY")
            buzzer_key = self.buzzer.wait_for_buzz()

            if not self._is_valid_buzz(buzzer_key, first_buzzer, attempts):
                continue

            player = self.players[buzzer_key]
            print(f"{player.name} buzzed in.")

            if attempts == 0:
                first_buzzer = buzzer_key

            user_answer = BuzzerInput.get_valid_answer()
            attempts += 1

            if user_answer == question.answer:
                player.add_point()
                if attempts == 1:
                    print(f"Correct. +1 point to {player.name}")
                else:
                    print(f"Correct! Steal successful. +1 point to {player.name}")
                break
            else:
                if attempts == 1:
                    print("Incorrect. Steal opportunity available.")
                else:
                    print(f"Incorrect. The correct answer was {question.answer}")
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
            print(f"\nKey {buzzer_key} is not assigned to a player.")
            return False

        if attempts == 1 and buzzer_key == first_buzzer:
            print(f"{self.players[buzzer_key].name} already attempted "
                  f"this question.")
            return False

        return True

    def _display_current_scores(self):
        """Display current scores for all players."""
        print("\n" + "-" * 50)
        print("CURRENT SCORES:")
        for player in sorted(self.players.values(), key=lambda p: p.key):
            print(f"  {player.name}: {player.score}")
        print("-" * 50)

    def _display_winner(self, sorted_players: List[Player]):
        """Display the game winner."""
        if sorted_players:
            winner = sorted_players[0]
            print(f"\nWinner: {winner.name} with {winner.score} points!")


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

    print("\n=== OLDHAM QUIZ ===")
    print("Copyright (C) 2026 DecBr1")
    print("This program comes with ABSOLUTELY NO WARRANTY; for details type 'w'.")
    print("This is free software, and you are welcome to redistribute it under certain conditions; for details type 'c'.\n")
    response = input("Press Enter to continue, or type 'w' or 'c': ").strip().lower()
    if response == 'w':
        show_warranty()
        input("\nPress Enter to continue...")
    elif response == 'c':
        show_conditions()
        input("\nPress Enter to continue...")

    print()
    num_players = 0
    while num_players < 1 or num_players > 3:
        try:
            num_players = int(input("How many players? (1-3): "))
            if num_players < 1 or num_players > 3:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")

    print()  # Add blank line for spacing

    if num_players == 1:
        game = SinglePlayerGame(questions, num_players)
    else:
        game = MultiPlayerGame(questions, num_players)

    game.run()


if __name__ == "__main__":

    main()
