from typing import Optional


class FatError(Exception):
    """Exception raised by this application."""

    def __init__(self, message: str, extra: Optional[dict[str, str]] = None) -> None:
        """Initialize the exception.

        Args:
            message (str): The actual error message
            extra (Optional[dict[str, str]], optional): Optional dictionary with more information. Defaults to None.
        """
        super().__init__(message)

        self.message = message
        self.extra = extra or {}
