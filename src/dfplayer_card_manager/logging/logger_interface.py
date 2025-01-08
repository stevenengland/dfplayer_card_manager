from abc import ABC, abstractmethod

from dfplayer_card_manager.logging.verbosity_level import VerbosityLevel


class LoggerInterface(ABC):
    @property
    @abstractmethod
    def verbosity(self) -> VerbosityLevel:
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def fatal(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:  # noqa: WPS110
        pass

    @abstractmethod
    def trace(self, message: str) -> None:
        pass

    @abstractmethod
    def warn(self, message: str) -> None:
        pass
