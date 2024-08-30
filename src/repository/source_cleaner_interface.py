from abc import ABC, abstractmethod


class SdCardCleanerInterface(ABC):
    @abstractmethod
    def get_unwanted_root_dir_entries(self, sd_root_path: str) -> list[str]:
        pass
