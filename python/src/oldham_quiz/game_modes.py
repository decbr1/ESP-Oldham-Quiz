"""Game modes: base class and implementations."""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from .colours import Colours
from .colours import c
from .models import Player, Question
from .input_handler import BuzzerInput
from .database import HighScoreDatabase


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
                  "`python3 old_main_bkp.py` in a terminal.")
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
            print(f"\n{c(f'Winner: {winner.name} with {winner.score} points!').green.bold}")

    def get_game_mode(self) -> str:
        """Return the game mode identifier."""
        return 'multiplayer'

