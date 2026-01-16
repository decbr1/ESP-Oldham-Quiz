"""Pandas Dataframe functionality"""

import os
import sys
from typing import Optional

try:
    from .logger import *
    from .colours import c
    from .display_strategies import dataframe_display
    from .database import HighScoreDatabase
except:
    from logger import *
    from colours import c
    from display_strategies import dataframe_display
    from database import HighScoreDatabase

try:
    import pandas as pd
except:
    critical("pandas is not installed in this environment")
    sys.exit()

class HighScoreDataframe:
    """Manages high scores using Pandas dataframe"""

    def __init__(self, db: HighScoreDatabase):
        """
        Initialize with an existing database instance.

        Args:
            db: HighScoreDatabase instance to pull data from
        """
        self.db = db

    def get_dataframe(self, limit: int = 10, game_mode: Optional[str] = None, sort_by: str = 'score') -> pd.DataFrame:
        """
        Get high scores as a pandas DataFrame.

        Args:
            limit: Maximum number of scores to return
            game_mode: Filter by game mode ('single', 'multiplayer', or None for all)
            sort_by: Sort method - 'score' (by percentage/score, descending) or 'name' (alphabetically by player_name)

        Returns:
            Pandas Dataframe of requested scores, sorted as specified
        """

        data = self.db.get_top_scores(limit=limit, game_mode=game_mode)
        df = pd.DataFrame(data)

        if df.empty:
            return df

        if sort_by == 'name':
            df = df.sort_values(by='player_name', ascending=True)
        else:
            df = df.sort_values(by=['percentage', 'score'], ascending=[False, False])

        return df.reset_index(drop=True)

    def display_stats(self):
        """stdPrints statistical analysis of high scores."""

        df = self.get_dataframe(limit=None)
        print(df.describe())

    def display_leaderboard(self, limit: int = 10, game_mode: Optional[str] = None):
        """
        Display leaderboard using pandas DataFrame formatting.

        Args:
            limit: Maximum number of scores to display
            game_mode: Filter by 'single', 'multiplayer', or None for all
        """
        scores = self.db.get_top_scores(limit, game_mode)
        dataframe_display(scores, game_mode)
