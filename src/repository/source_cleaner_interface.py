from abc import ABC, abstractmethod


class SourceCleanerInterface(ABC):
    @abstractmethod
    def get_unwanted_root_dir_entries(self, sd_root_path: str) -> list[str]:
        pass

    @abstractmethod
    def delete_unwanted_root_dir_entries(self, file_paths: list[str]) -> None:
        pass

    @abstractmethod
    def get_root_dir_numbering_gaps(self, sd_root_path: str) -> list[int]:
        pass
