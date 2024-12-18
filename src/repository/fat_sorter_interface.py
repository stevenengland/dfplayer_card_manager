from abc import ABC, abstractmethod
from io import BytesIO


class FatSorterInterface(ABC):
    @abstractmethod
    def sort_fat_root(self, root_dir: str | BytesIO) -> None:
        pass
