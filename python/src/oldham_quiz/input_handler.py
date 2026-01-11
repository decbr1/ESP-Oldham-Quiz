"""Input handling for buzzer and keyboard input."""

import sys
import os

from .colours import c

# Platform-specific key press detection
if sys.platform.startswith('win'):
    import msvcrt
else:
    import tty
    import termios


class BuzzerInput:
    """Handles buzzer input detection across different platforms."""

    VALID_KEYS = ('Q', 'P', 'B')

    def __init__(self):
        """Initialize buzzer input handler."""
        self.is_tty = os.isatty(sys.stdin.fileno())

    def wait_for_buzz(self) -> str:
        """
        Wait for a valid buzzer key press.

        Returns:
            The pressed key (Q, P, or B)
        """
        if sys.platform.startswith('win'):
            return self._wait_for_buzz_windows()
        else:
            return self._wait_for_buzz_unix()

    def _wait_for_buzz_windows(self) -> str:
        """Wait for buzzer key on Windows."""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').upper()
                if key in self.VALID_KEYS:
                    return key

    def _wait_for_buzz_unix(self) -> str:
        """Wait for buzzer key on Unix-like systems."""
        if not self.is_tty:
            # Fallback for IDE/non-TTY environments
            return self._wait_for_buzz_fallback()

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                key = sys.stdin.read(1).upper()
                if key in self.VALID_KEYS:
                    return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _wait_for_buzz_fallback(self) -> str:
        """Fallback input method for non-TTY environments."""
        while True:
            key = input("").upper().strip()
            if key in self.VALID_KEYS:
                return key
            print(c(f"Invalid key! Please enter {', '.join(self.VALID_KEYS)}.").red)

    @staticmethod
    def get_valid_answer() -> str:
        """
        Get a valid answer (A, B, or C) from the user.

        Returns:
            The user's answer choice
        """
        while True:
            user_answer = input("Answer >> ").upper().strip()
            if user_answer in ('A', 'B', 'C'):
                return user_answer
            else:
                print(c("Invalid input! Please enter A, B, or C.").red)

