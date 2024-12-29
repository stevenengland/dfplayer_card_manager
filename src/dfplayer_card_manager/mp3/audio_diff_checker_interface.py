from abc import ABC, abstractmethod

from dfplayer_card_manager.mp3.tag_collection import TagCollection


class AudioDiffCheckerInterface(ABC):
    @abstractmethod
    def check_diff_by_hash(
        self,
        audio_file_path: str,
        audio_file_path_compare: str,
    ) -> bool:
        pass

    @abstractmethod
    def check_diff_by_tags(self, audio_dir_path: str, tags: TagCollection) -> bool:
        pass
