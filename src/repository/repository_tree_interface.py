from abc import ABC, abstractmethod


class RepositoryTreeInterface(ABC):
    @abstractmethod
    def get_target_tree(self, sd_root_path: str) -> list[str]:
        pass

    @abstractmethod
    def get_valid_root_dirs(self, root_dir: str, valid_dir_pattern: str) -> list[str]:
        pass

    @abstractmethod
    def get_valid_subdir_files(self, subdir: str, valid_file_pattern: str) -> list[str]:
        pass
