import hashlib

from dfplayer_card_manager.mp3.audio_diff_checker_interface import (
    AudioDiffCheckerInterface,
)
from dfplayer_card_manager.mp3.audio_file_manager import (
    AudioFileManagerInterface,
)
from dfplayer_card_manager.mp3.tag_collection import TagCollection


class AudioDiffChecker(AudioDiffCheckerInterface):
    # init with a exed3 tag manager
    def __init__(self, audio_file_manager: AudioFileManagerInterface):
        self.audio_file_manager = audio_file_manager

    def check_diff_by_hash(
        self,
        audio_file_path: str,
        audio_file_path_compare: str,
    ) -> bool:
        # read the audio content of the files
        audio_content = self.audio_file_manager.read_audio_content(audio_file_path)
        audio_content_compare = self.audio_file_manager.read_audio_content(
            audio_file_path_compare,
        )

        # hash the audio content and compare the hashes
        return (
            hashlib.md5(audio_content, usedforsecurity=False).hexdigest()
            == hashlib.md5(audio_content_compare, usedforsecurity=False).hexdigest()
        )

    def check_diff_by_tags(self, audio_dir_path: str, tags: TagCollection) -> bool:
        read_tags = self.audio_file_manager.read_id3_tags(audio_dir_path)

        # compare the public attributes album, title, track_number and artist and return true if they are equal
        return all(
            getattr(tags, attr) == getattr(read_tags, attr)
            for attr in ("album", "title", "track_number", "artist")
        )
