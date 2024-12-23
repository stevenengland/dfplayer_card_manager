import hashlib

from src.mp3.audio_diff_checker_interface import AudioDiffCheckerInterface
from src.mp3.audio_file_manager import AudioFileManager
from src.mp3.tag_collection import TagCollection


class AudioDiffChecker(AudioDiffCheckerInterface):
    # init with a exed3 tag manager
    def __init__(self, tag_manager: AudioFileManager):
        self.tag_manager = tag_manager

    def check_diff_by_hash(
        self,
        audio_file_path: str,
        audio_file_path_compare: str,
    ) -> bool:
        # read the audio content of the files
        audio_content = self.tag_manager.read_audio_content(audio_file_path)
        audio_content_compare = self.tag_manager.read_audio_content(
            audio_file_path_compare,
        )

        # hash the audio content and compare the hashes
        return (
            hashlib.md5(audio_content, usedforsecurity=False).hexdigest()
            == hashlib.md5(audio_content_compare, usedforsecurity=False).hexdigest()
        )

    def check_diff_by_tags(self, audio_dir_path: str, tags: TagCollection) -> bool:
        read_tags = self.tag_manager.read_id3_tags(audio_dir_path)

        # compare the public attributes album, title, track_number and artist and return true if they are equal
        return all(
            getattr(tags, attr) == getattr(read_tags, attr)
            for attr in ("album", "title", "track_number", "artist")
        )
