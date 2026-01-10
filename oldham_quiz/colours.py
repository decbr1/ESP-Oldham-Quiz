"""ANSI color codes for terminal output."""


class Colours:
    """ANSI colour codes for terminal output."""
    # Basic Colours
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Reset
    RESET = '\033[0m'

    @staticmethod
    def disable():
        """Disable Colours (for non-ANSI terminals)."""
        Colours.RED = ''
        Colours.GREEN = ''
        Colours.YELLOW = ''
        Colours.BLUE = ''
        Colours.MAGENTA = ''
        Colours.CYAN = ''
        Colours.WHITE = ''
        Colours.BOLD = ''
        Colours.UNDERLINE = ''
        Colours.RESET = ''

