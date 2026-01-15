import os
import sys

from python.src.oldham_quiz import HighScoreDatabase
from python.src.oldham_quiz.logger import *

try:
    import pandas as pd
except:
    critical("pandas is not installed in this environment")
    sys.exit()

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
db_path = os.path.join(project_root, 'high_scores.db')

high_score_db = HighScoreDatabase(db_path)

data = high_score_db.get_top_scores(limit=10, game_mode=None)
df = pd.DataFrame(data)

print(df)