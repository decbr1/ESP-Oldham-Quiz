"""High score database management using SQLite."""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

from .display_strategies import simple_display, LeaderboardDisplay

try:
    from .colours import c
except:
    from colours import c

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

    def display_leaderboard(self, limit: int = 10, game_mode: Optional[str] = None,
                            display_fn: Optional[LeaderboardDisplay] = None):
        """Display leaderboard using specified display function.

        Args:
            limit: Maximum number of scores to display
            game_mode: Filter by 'single', 'multiplayer', or None for all
            display_fn: Optional display function to use (defaults to simple_display)
        """
        scores = self.get_top_scores(limit, game_mode)
        display = display_fn or simple_display
        display(scores, game_mode)

