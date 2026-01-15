"""Display strategies for leaderboards."""

import sys
from typing import Optional, List, Dict, Callable

try:
    from .logger import critical
    from .colours import c
except ImportError:
    from logger import critical
    from colours import c


# Type alias for any function that displays a leaderboard
LeaderboardDisplay = Callable[[List[Dict], Optional[str]], None]


def simple_display(scores: List[Dict], game_mode: Optional[str] = None) -> None:
    """Display leaderboard using simple text formatting.

    This function prints a nicely formatted leaderboard to the console using
    basic text formatting and ANSI color codes.

    Args:
        scores: List of score dictionaries. Each dictionary should contain:
            - player_name (str): Name of the player
            - score (int): Number of correct answers
            - total_questions (int): Total questions asked
            - percentage (float): Score as a percentage
            - game_mode (str): 'single' or 'multiplayer'
            - timestamp (str): When the score was recorded
        game_mode: Optional filter for game mode. If provided, adds mode
            indicator to the title. Use 'single', 'multiplayer', or None
            for all modes.

    Returns:
        None. Prints directly to stdout.

    Example:
        >>> scores = [{'player_name': 'Alice', 'score': 8, ...}]
        >>> simple_display(scores, game_mode='single')
        ======================================================================
        HIGH SCORES LEADERBOARD (SINGLE)
        ======================================================================
         1. Alice                 8/10 (80.0%)  [S]  2024-01-15
        ======================================================================
    """
    if not scores:
        print(f"\n{c('No high scores yet. Be the first!').yellow}\n")
        return

    # Build title with optional game mode indicator
    mode_text = f" ({game_mode.upper()})" if game_mode else " (ALL MODES)"

    print("\n" + "=" * 70)
    print(c(f"HIGH SCORES LEADERBOARD{mode_text}").bold.magenta)
    print("=" * 70)

    # Print each score entry
    for rank, score_data in enumerate(scores, 1):
        # Convert game mode to single-letter badge
        mode_badge = "[S]" if score_data['game_mode'] == 'single' else "[M]"

        # Extract just the date (ignore time)
        timestamp = score_data['timestamp'].split()[0]

        # Format: rank, name, score, percentage, mode, date
        print(f"{c(f'{rank:2d}. {score_data['player_name']:<20}').cyan} "
              f"{c(f'{score_data['score']:2d}/{score_data['total_questions']:2d}').bold} "
              f"({score_data['percentage']:5.1f}%)  "
              f"{c(mode_badge).yellow}  "
              f"{c(timestamp).white}")

    print("=" * 70)
    print(f"{c('Legend: [S] = Single Player, [M] = Multiplayer').white}\n")


def dataframe_display(scores: List[Dict], game_mode: Optional[str] = None) -> None:
    """Display leaderboard using pandas DataFrame formatting.

    This function converts the scores to a pandas DataFrame and uses pandas'
    built-in formatting for display. Requires pandas to be installed.

    Args:
        scores: List of score dictionaries. Each dictionary should contain:
            - player_name (str): Name of the player
            - score (int): Number of correct answers
            - total_questions (int): Total questions asked
            - percentage (float): Score as a percentage
            - game_mode (str): 'single' or 'multiplayer'
            - timestamp (str): When the score was recorded
        game_mode: Optional filter for game mode. Currently not used in
            formatting but kept for API consistency.

    Returns:
        None. Prints directly to stdout.

    Raises:
        SystemExit: If pandas is not installed in the environment.

    Example:
        >>> scores = [{'player_name': 'Alice', 'score': 8, ...}]
        >>> dataframe_display(scores)
        ======================================================================
        HIGH SCORES LEADERBOARD
        ======================================================================
        player_name  score  total_questions  percentage  game_mode  timestamp
        Alice            8               10        80.0     single  2024-01-15
        ======================================================================
    """
    try:
        import pandas as pd
    except ImportError:
        critical("pandas is not installed in this environment")
        sys.exit(1)

    df = pd.DataFrame(scores)

    if df.empty:
        print(f"\n{c('No high scores yet. Be the first!').yellow}\n")
        return

    print("\n" + "=" * 70)
    print(c("HIGH SCORES LEADERBOARD").bold.magenta)
    print("=" * 70)
    print(df.to_string(index=False))
    print("=" * 70 + "\n")
