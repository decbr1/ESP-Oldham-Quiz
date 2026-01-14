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


class ColouredStr(str):
    def __getattr__(self, name):
        color_methods = {
            'red': Colours.RED, 'green': Colours.GREEN, 'yellow': Colours.YELLOW,
            'blue': Colours.BLUE, 'magenta': Colours.MAGENTA, 'cyan': Colours.CYAN,
            'white': Colours.WHITE, 'bold': Colours.BOLD, 'underline': Colours.UNDERLINE
        }
        if name in color_methods:
            return ColouredStr(f'{color_methods[name]}{self}{Colours.RESET}')
        raise AttributeError(f"'ColouredStr' object has no attribute '{name}'")

def c(text): return ColouredStr(text)

# print(c("test").red.bold)
# print(c("success").green)
