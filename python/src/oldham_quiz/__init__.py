"""
Oldham Quiz - A multi-player quiz game with buzzer support.

This package implements a quiz game that supports both single-player and
multi-player modes with buzzer functionality for competitive play.
"""

from .colours import Colours, ColouredStr, c
from .database import HighScoreDatabase
from .dataframe import HighScoreDataframe
from .models import Player, Question
from .input_handler import BuzzerInput
from .game_modes import QuizGame, SinglePlayerGame, MultiPlayerGame
from .utils import load_questions, show_warranty, show_conditions

__version__ = '1.0.0'
__all__ = [
    'Colours',
    'ColouredStr',
    'c',
    'HighScoreDatabase',
    'HighScoreDataframe',
    'Player',
    'Question',
    'BuzzerInput',
    'QuizGame',
    'SinglePlayerGame',
    'MultiPlayerGame',
    'load_questions',
    'show_warranty',
    'show_conditions',
]