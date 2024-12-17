from abc import ABC, abstractmethod
from typing import Optional

from src.repository.repository_element import RepositoryElement


class DfPlayerCardManagerInterface(ABC):
    @property
    @abstractmethod
    def source_repo(self) -> list[RepositoryElement]:
        pass

    @property
    @abstractmethod
    def target_repo(self) -> list[RepositoryElement]:
        pass

    @abstractmethod
    def init_repositories(self):
        pass

    @abstractmethod
    def get_target_repository_tree(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def get_source_repository_tree(
        self,
        valid_subdir_files_pattern_overrides: Optional[dict[str, str]] = None,
    ) -> list[tuple[str, str]]:
        pass
