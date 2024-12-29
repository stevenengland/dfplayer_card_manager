from abc import ABC, abstractmethod

from dfplayer_card_manager.config.configuration import (
    Configuration,
    RepositoryConfig,
)
from dfplayer_card_manager.repository.compare_results import CompareResult
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


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

    @abstractmethod
    def get_repositories_comparison(self) -> list[tuple[int, int, CompareResult]]:
        pass

    @abstractmethod
    def write_copy_to_target_repository(
        self,
        dir_number: int,
        track_number: int,
    ) -> None:
        pass
