import shutil
from typing import Optional, Tuple

import eyed3

from dfplayer_card_manager.mp3.audio_file_manager_interface import (
    AudioFileManagerInterface,
)
from dfplayer_card_manager.mp3.tag_collection import TagCollection
from dfplayer_card_manager.mp3.tag_error import TagError

eyed3.log.setLevel("ERROR")


class AudioFileManager(AudioFileManagerInterface):

    def read_audio_content_and_id3_tags(
        self,
        file_path: str,
        check_tags: bool = True,
    ) -> Tuple[bytes, TagCollection]:
        # ToDo: Refactor this method to use only one read audio method
        audio = self._read_audio(file_path)
        if check_tags:
            self._check_tags(audio)

        tag_collection = self._extract_tags(audio)
        audio_content = self._extract_audio_content(file_path, audio)
        return audio_content, tag_collection

    def read_id3_tags(
        self,
        file_path: str,
        check_tags: bool = True,
    ) -> TagCollection:
        audio = self._read_audio(file_path)
        if check_tags:
            self._check_tags(audio)

        return self._extract_tags(audio)

    def read_audio_content(self, file_path: str) -> bytes:
        audio = self._read_audio(file_path)

        return self._extract_audio_content(file_path, audio)

    def copy_audio(
        self,
        source_path: str,
        target_path: str,
        tags_to_append: Optional[TagCollection] = None,
    ) -> None:
        if not tags_to_append:
            tags_to_append = TagCollection()

        # copy source file to target file
        shutil.copyfile(source_path, target_path)

        # read audio from target file
        audio = self._read_audio(target_path)
        if not audio.tag:
            audio.initTag()
        audio.tag.artist = tags_to_append.artist or audio.tag.artist
        audio.tag.title = tags_to_append.title or audio.tag.title
        audio.tag.album = tags_to_append.album or audio.tag.album
        audio.tag.track_num = (
            tags_to_append.track_number or audio.tag.track_num[0],
            None,  # total number of tracks
        )

        audio.tag.save()

    def _check_tags(self, audio: eyed3.AudioFile) -> None:
        if not audio.tag or audio.tag.version[0] != 2:
            raise TagError(f"Invalid or unsupported audio tag for file {audio.path}")

    def _read_audio(self, file_path: str) -> eyed3.AudioFile:
        audio = eyed3.load(file_path)
        if not audio:
            raise TagError(f"Could not load audio file {file_path}")
        return audio

    def _extract_tags(self, audio: eyed3.AudioFile) -> TagCollection:
        tag_collection = TagCollection()
        if not audio.tag:
            return tag_collection
        tag_collection.title = audio.tag.title
        tag_collection.artist = audio.tag.artist
        tag_collection.album = audio.tag.album
        tag_collection.track_number = audio.tag.track_num[0]
        return tag_collection

    def _extract_audio_content(self, file_path: str, audio: eyed3.AudioFile) -> bytes:
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
