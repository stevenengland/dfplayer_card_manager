import eyed3
import pytest

from src.mp3.audio_file_manager_interface import AudioFileManagerInterface
from src.mp3.tag_collection import TagCollection
from src.mp3.tag_error import TagError

pytestmark = pytest.mark.usefixtures("unstub")


class AudioFileManager(AudioFileManagerInterface):

    def read_id3_tags(self, file_path: str) -> TagCollection:
        audio = eyed3.load(file_path)

        self._check_file(audio)

        tag_collection = TagCollection()
        # Check if ID3v2 tag exists and is version 2.4
        tag_collection.title = audio.tag.title
        tag_collection.artist = audio.tag.artist
        tag_collection.album = audio.tag.album
        tag_collection.track_number = audio.tag.track_num[0]
        return tag_collection

    def read_audio_content(self, file_path: str) -> bytes:
        audio = eyed3.load(file_path)

        self._check_file(audio)

        metadata_size = 0
        if audio.tag and audio.tag.file_info:
            # Seek past ID3v2 tag
            metadata_size = (
                audio.tag.file_info.tag_size  # without tag_padding_size that is included in tag_size
            )

        with open(file_path, "rb") as audio_file_stream:
            audio_file_stream.seek(metadata_size)
            audio_content = audio_file_stream.read()
        return audio_content

    def _check_tags(self, audio: eyed3.AudioFile) -> bool:
        return audio.tag and audio.tag.version[0] == 2

    def _check_audio(self, audio: eyed3.AudioFile) -> bool:
        return bool(audio)

    def _check_file(self, audio: eyed3.AudioFile) -> None:
        if not self._check_audio(audio):
            raise ValueError("Could not load MP3 file")
        if not self._check_tags(audio):
            raise TagError("Invalid or unsupported audio tag.")
