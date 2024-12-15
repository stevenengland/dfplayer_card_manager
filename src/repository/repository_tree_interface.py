from abc import ABC, abstractmethod


class RepositoryTreeInterface(ABC):
    @abstractmethod
    def get_target_tree(self, sd_root_path: str) -> list[str]:
        pass

    @abstractmethod
    def get_valid_subdirs(self, root_dir: str) -> list[str]:
        pass
