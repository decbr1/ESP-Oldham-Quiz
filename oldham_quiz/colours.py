"""ANSI colour codes for terminal output."""


class Colours:
    """ANSI colour codes for terminal output."""

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

    def red_str(this, msg): return f"{this.RED}{msg}{this.RESET}"
    def green_str(this, msg): return f"{this.GREEN}{msg}{this.RESET}"
    def yellow_str(this, msg): return f"{this.YELLOW}{msg}{this.RESET}"
    def blue_str(this, msg): return f"{this.BLUE}{msg}{this.RESET}"
    def magenta_str(this, msg): return f"{this.MAGENTA}{msg}{this.RESET}"
    def cyan_str(this, msg): return f"{this.CYAN}{msg}{this.RESET}"
    def white_str(this, msg): return f"{this.WHITE}{msg}{this.RESET}"
    def bold_str(this, msg): return f"{this.BOLD}{msg}{this.RESET}"
    def underline_str(this, msg): return f"{this.UNDERLINE}{msg}{this.RESET}"

    def red(this, msg): print(this.red_str(this, msg))
    def green(this, msg): print(this.green_str(this, msg))
    def yellow(this, msg): print(this.yellow_str(this, msg))
    def blue(this, msg): print(this.blue_str(this, msg))
    def magenta(this, msg): print(this.magenta_str(this, msg))
    def cyan(this, msg): print(this.cyan_str(this, msg))
    def white(this, msg): print(this.white_str(this, msg))
    def bold(this, msg): print(this.bold_str(this, msg))
    def underline(this, msg): print(this.underline_str(this, msg))


print(Colours.bold_str(Colours, Colours.red_str(Colours, "test")))

Colours.bold(Colours, Colours.red_str(Colours, "test1"))
