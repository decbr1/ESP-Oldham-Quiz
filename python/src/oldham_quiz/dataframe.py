"""Pandas Dataframe functionality"""

import os
import sys
from typing import Optional

from logger import *
from database import HighScoreDatabase


try:
    import pandas as pd
except:
    critical("pandas is not installed in this environment")
    sys.exit()

class HighScoreDataframe(HighScoreDatabase):
    """Manages high scores using Pandas dataframe"""

    def __init__(self, db: HighScoreDatabase):
        """
        Initialize with an existing database instance.

        Args:
            db: HighScoreDatabase instance to pull data from
        """
        self.db = db

    def get_dataframe(self, limit: int = 10, game_mode: Optional[str] = None) -> pd.DataFrame:
        """Get high scores as a pandas DataFrame."""
        data = self.db.get_top_scores(limit=limit, game_mode=game_mode)
        return pd.DataFrame(data)

    def display_stats(self):
        """Display statistical analysis of high scores."""
        df = self.get_dataframe(limit=None)
        print(df.describe())


