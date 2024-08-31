from abc import ABC, abstractmethod

from src.mp3.tag_collection import TagCollection


class TagManagerInterface(ABC):
    @abstractmethod
    def read_id3_tags(self, file_path: str) -> TagCollection:
        pass
