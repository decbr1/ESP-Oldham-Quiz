"""ANSI colour codes for terminal output."""

class Colours:
    """ANSI colour codes for terminal output."""
    RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
    BLUE = '\033[94m'; MAGENTA = '\033[95m'; CYAN = '\033[96m'
    WHITE = '\033[97m'; BOLD = '\033[1m'; UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    def __init__(self): self._codes = []

    @staticmethod
    def disable():
        """Disable Colours (for non-ANSI terminals)."""
        Colours.RED = ''; Colours.GREEN = ''; Colours.YELLOW = ''
        Colours.BLUE = ''; Colours.MAGENTA = ''; Colours.CYAN = ''
        Colours.WHITE = ''; Colours.BOLD = ''; Colours.UNDERLINE = ''
        Colours.RESET = ''

    def red(self): self._codes.append(self.RED); return self
    def green(self): self._codes.append(self.GREEN); return self
    def yellow(self): self._codes.append(self.YELLOW); return self
    def blue(self): self._codes.append(self.BLUE); return self
    def magenta(self): self._codes.append(self.MAGENTA); return self
    def cyan(self): self._codes.append(self.CYAN); return self
    def white(self): self._codes.append(self.WHITE); return self
    def bold(self): self._codes.append(self.BOLD); return self
    def underline(self): self._codes.append(self.UNDERLINE); return self

    def format(self, msg): return f"{''.join(self._codes)}{msg}{self.RESET}"
    def print(self, msg): print(self.format(msg))


class Style:
    def __init__(self, text):
        self.text = text
        self.codes = []

    def red(self): self.codes.append(Colours.RED); return self
    def green(self): self.codes.append(Colours.GREEN); return self
    def yellow(self): self.codes.append(Colours.YELLOW); return self
    def blue(self): self.codes.append(Colours.BLUE); return self
    def magenta(self): self.codes.append(Colours.MAGENTA); return self
    def cyan(self): self.codes.append(Colours.CYAN); return self
    def white(self): self.codes.append(Colours.WHITE); return self
    def bold(self): self.codes.append(Colours.BOLD); return self
    def underline(self): self.codes.append(Colours.UNDERLINE); return self

    def __str__(self): return f"{''.join(self.codes)}{self.text}{Colours.RESET}"

def style(msg): return Style(msg)


print(style("test").red().bold())
print(style("success").green())
