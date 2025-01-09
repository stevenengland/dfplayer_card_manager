from abc import ABC, abstractmethod
from typing import Optional, Tuple

from dfplayer_card_manager.mp3.tag_collection import TagCollection


class AudioFileManagerInterface(ABC):
    @abstractmethod
    def read_audio_content_and_id3_tags(
        self,
        file_path: str,
        check_tags: bool = True,
    ) -> Tuple[bytes, TagCollection]:
        pass

    @abstractmethod
    def read_id3_tags(
        self,
        file_path: str,
        check_tags: bool = True,
    ) -> TagCollection:
        pass

    @abstractmethod
    def read_audio_content(self, file_path: str) -> bytes:
        pass

    @abstractmethod
    def copy_audio(
        self,
        source_path: str,
        target_path: str,
        tags_to_append: Optional[TagCollection] = None,
    ) -> None:
        pass
