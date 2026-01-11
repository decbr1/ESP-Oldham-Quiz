"""Data models for players and questions."""

from .colours import c

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
        print(f"\n{c(f'Question {self.index}:').cyan.bold} {c(self.text).white}")
        for option in self.options:
            print(f"  {c(option).yellow}")

