from abc import ABC, abstractmethod
from io import BytesIO


class FatSorterInterface(ABC):
    @abstractmethod
    def is_fat_volume_sorted(self, root_dir: str | BytesIO) -> bool:
        pass

    @abstractmethod
    def sort_fat_dir(self, root_dir: str | BytesIO) -> None:
        pass

    @abstractmethod
    def sort_fat_volume(self, root_dir: str | BytesIO) -> None:
        pass
