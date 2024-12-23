from abc import ABC, abstractmethod

from src.config.configuration import Configuration, RepositoryConfig
from src.repository.repository_element import RepositoryElement


class DfPlayerCardManagerInterface(ABC):
    @property
    @abstractmethod
    def config(self) -> Configuration:
        pass

    @property
    @abstractmethod
    def source_repo(self) -> list[RepositoryElement]:
        pass

    @property
    @abstractmethod
    def target_repo(self) -> list[RepositoryElement]:
        pass

    @property
    @abstractmethod
    def config_overrides(self) -> dict[str, RepositoryConfig]:
        pass

    @abstractmethod
    def create_repositories(self) -> None:
        pass

    @abstractmethod
    def read_config(self) -> Configuration:
        pass

    @abstractmethod
    def read_config_overrides(self) -> dict[str, RepositoryConfig]:
        pass
