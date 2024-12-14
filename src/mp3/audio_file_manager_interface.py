from abc import ABC, abstractmethod

from src.mp3.tag_collection import TagCollection


class AudioFileManagerInterface(ABC):
    @abstractmethod
    def read_id3_tags(self, file_path: str) -> TagCollection:
        pass

    @abstractmethod
    def read_audio_content(self, file_path: str) -> bytes:
        pass
