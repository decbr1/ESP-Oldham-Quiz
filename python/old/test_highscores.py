#!/usr/bin/env python3
"""Test script for high score database."""

from old_main_bkp import HighScoreDatabase
import os

# Test the database
db = HighScoreDatabase('test_scores.db')

# Add some test scores
db.add_score('Alice', 18, 20, 'single')
db.add_score('Bob', 15, 20, 'multiplayer')
db.add_score('Charlie', 20, 20, 'single')
db.add_score('Diana', 17, 20, 'multiplayer')
db.add_score('Eve', 19, 20, 'single')

print('Test scores added!')
print()
db.display_leaderboard()
print()
print('Single player leaderboard:')
db.display_leaderboard(game_mode='single')
print()
print('Multiplayer leaderboard:')
db.display_leaderboard(game_mode='multiplayer')

# Clean up test database
os.remove('test_scores.db')
print('\nTest completed successfully!')

