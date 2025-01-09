from abc import ABC, abstractmethod

from dfplayer_card_manager.config.configuration import (
    Configuration,
    RepositoryConfig,
)
from dfplayer_card_manager.repository.compare_result import CompareResult
from dfplayer_card_manager.repository.repository import Repository


class DfPlayerCardManagerInterface(ABC):  # noqa: WPS214
    @property
    @abstractmethod
    def config(self) -> Configuration:
        pass

    @property
    @abstractmethod
    def source_repo(self) -> Repository:
        pass

    @property
    @abstractmethod
    def source_repo_root_dir(self) -> str:
        pass

    @property
    @abstractmethod
    def target_repo(self) -> Repository:
        pass

    @property
    @abstractmethod
    def target_repo_root_dir(self) -> str:
        pass

    @property
    @abstractmethod
    def config_overrides(self) -> dict[str, RepositoryConfig]:
        pass

    @abstractmethod
    def create_repositories(self) -> None:
        pass

    @abstractmethod
    def get_repositories_comparison(self) -> list[CompareResult]:
        pass

    @abstractmethod
    def write_change_to_target_repository(self, compare_result: CompareResult) -> None:
        pass
