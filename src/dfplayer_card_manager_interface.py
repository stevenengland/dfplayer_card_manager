from abc import ABC, abstractmethod
from typing import Optional


class DfPlayerCardManagerInterface(ABC):
    @abstractmethod
    def get_target_repository_tree(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def get_source_repository_tree(
        self,
        valid_subdir_files_pattern_overrides: Optional[dict[str, str]] = None,
    ) -> list[tuple[str, str]]:
        pass

    @abstractmethod

