from rich.console import Console
from rich.theme import Theme

from dfplayer_card_manager.logging.logger_interface import LoggerInterface
from dfplayer_card_manager.logging.verbosity_level import VerbosityLevel


class Logger(LoggerInterface):
    def __init__(self, verbosity: VerbosityLevel = VerbosityLevel.info) -> None:
        self._verbosity = verbosity
        # Create themed console for different message types
        self.console = Console(
            theme=Theme(
                {
                    "trace": "dim cyan",
                    "debug": "blue",
                    "info": "white",
                    "warn": "yellow",
                    "error": "red",
                    "fatal": "red bold",
                },
            ),
        )

    @property
    def verbosity(self) -> VerbosityLevel:
        return self._verbosity

    @verbosity.setter
    def verbosity(self, verbosity: VerbosityLevel) -> None:
        self._verbosity = verbosity

    def trace(self, message: str) -> None:
        """Print trace messages."""
        if self._verbosity >= VerbosityLevel.trace:
            self.console.print(f"[trace]T: [/trace] {message}")

    def debug(self, message: str) -> None:
        """Print debug messages only in DEBUG mode."""
        if self._verbosity >= VerbosityLevel.debug:
            self.console.print(f"[debug]D: [/debug] {message}")

    def info(self, message: str) -> None:  # noqa: WPS110
        """Print info messages."""
        if self._verbosity >= VerbosityLevel.info:
            self.console.print(f"[info]I: [/info] {message}")

    def warn(self, message: str) -> None:
        """Print warning messages."""
        if self._verbosity >= VerbosityLevel.warn:
            self.console.print(f"[warn]W: [/warn] {message}")

    def error(self, message: str) -> None:
        """Print error messages."""
        if self._verbosity >= VerbosityLevel.error:
            self.console.print(f"[error]E: [/error] {message}")

    def fatal(self, message: str) -> None:
        """Print fatal error messages."""
        if self._verbosity >= VerbosityLevel.fatal:
            self.console.print(f"[fatal]F: [/fatal] {message}")
