from abc import ABC, abstractmethod


class SourceCleanerInterface(ABC):
    @abstractmethod
    def get_unwanted_root_dir_entries(self, sd_root_path: str) -> list[str]:
        pass

    # Receives a list of file paths and deletes them
    @abstractmethod
    def delete_unwanted_root_dir_entries(self, file_paths: list[str]) -> None:
        pass
