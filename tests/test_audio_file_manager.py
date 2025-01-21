import os
import shutil
from unittest.mock import MagicMock, Mock

import eyed3
import pytest
from file_system_helper import FakeFileSystemHelper

from dfplayer_card_manager.mp3.audio_file_manager import (
    AudioFileManager,
    AudioFileManagerInterface,
)
from dfplayer_card_manager.mp3.tag_collection import TagCollection
from dfplayer_card_manager.mp3.tag_error import TagError

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def tag_manager() -> AudioFileManager:
    sut = AudioFileManager()
    return sut  # noqa: WPS331


class TestReadAudio:

    def test_read_id3_tags_with_valid_tags(self, sut: AudioFileManagerInterface, when):
        # GIVEN
        tag_mock = MagicMock()
        tag_mock.tag.version = (2, 4)
        tag_mock.tag.title = "Song Title"
        tag_mock.tag.artist = "Artist Name"
        tag_mock.tag.album = "Album Name"
        tag_mock.tag.track_num = (1,)
        when(eyed3).load(...).thenReturn(tag_mock)

        # WHEN
        sut_result = sut.read_id3_tags("file_path")

        # THEN
        assert isinstance(sut_result, TagCollection)
        assert sut_result.title == "Song Title"
        assert sut_result.artist == "Artist Name"
        assert sut_result.album == "Album Name"
        assert sut_result.track_number == 1

    def test_read_id3_tags_with_invalid_tags(
        self,
        sut: AudioFileManagerInterface,
        when,
    ):
        # GIVEN
        tag_mock = MagicMock()
        tag_mock.tag.version = (9,)

        when(eyed3).load(...).thenReturn(tag_mock)

        # WHEN
        # THEN
        with pytest.raises(expected_exception=TagError, match="Invalid"):
            sut.read_id3_tags("file_path")

    # @pytest.mark.skip(reason="no way of currently testing this")
    @e2e
    def test_read_id3_tags_from_file_wo_tags(
        self,
        sut: AudioFileManagerInterface,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        # WHEN
        # THEN
        tags = sut.read_id3_tags(
            os.path.join(test_assets_fs.test_assets_path, "0003.mp3"),
            check_tags=False,
        )

        assert tags.title is None

        with pytest.raises(expected_exception=TagError, match="Invalid"):
            sut.read_id3_tags(
                os.path.join(test_assets_fs.test_assets_path, "0003.mp3"),
            )

    # @pytest.mark.skip(reason="no way of currently testing this")
    @e2e
    def test_read_id3_tags_from_file_w_tags(
        self,
        sut: AudioFileManagerInterface,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        # WHEN
        sut_result = sut.read_id3_tags(
            os.path.join(test_assets_fs.test_assets_path, "0002.mp3"),
        )
        # THEN
        assert sut_result.title == "title_test"
        assert sut_result.artist == "artist_test"
        assert sut_result.album == "album_test"
        assert sut_result.track_number == 99

    # @pytest.mark.skip(reason="no way of currently testing this")
    @e2e
    def test_read_audio_content(
        self,
        sut: AudioFileManagerInterface,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        # WHEN
        sut_result_1 = sut.read_audio_content(
            os.path.join(test_assets_fs.test_assets_path, "0001.mp3"),
        )
        sut_result_2 = sut.read_audio_content(
            os.path.join(test_assets_fs.test_assets_path, "0002.mp3"),
        )
        # THEN

        assert len(sut_result_1) == 3605
        assert len(sut_result_2) == 3605

    @e2e
    def test_read_audio_content_and_id3_tags(
        self,
        sut: AudioFileManagerInterface,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        # WHEN
        sut_result_1, sut_result_2 = sut.read_audio_content_and_id3_tags(
            os.path.join(test_assets_fs.test_assets_path, "0002.mp3"),
        )

        # THEN
        assert len(sut_result_1) == 3605
        assert isinstance(sut_result_2, TagCollection)

    @e2e
    def test_read_audio_content_and_id3_tags_from_file_wo_tags(
        self,
        sut: AudioFileManagerInterface,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        # WHEN
        # THEN
        sut_result_1, sut_result_2 = sut.read_audio_content_and_id3_tags(
            os.path.join(test_assets_fs.test_assets_path, "0003.mp3"),
            check_tags=False,
        )

        assert len(sut_result_1) == 3605
        assert isinstance(sut_result_2, TagCollection)

        with pytest.raises(expected_exception=TagError, match="Invalid"):
            sut_result_1, sut_result_2 = sut.read_audio_content_and_id3_tags(
                os.path.join(test_assets_fs.test_assets_path, "0003.mp3"),
            )


class TestCopyingAudio:
    def test_copy_audio(
        self,
        sut: AudioFileManagerInterface,
        when,
    ):
        # GIVEN
        source_file_path = os.path.join("source_root", "01", "01.mp3")
        target_file_path = os.path.join("target_root", "01", "01.mp3")
        tags_to_append = TagCollection()
        tags_to_append.artist = "artist_test"
        tags_to_append.title = "title_test"
        tags_to_append.album = "album_test"
        tags_to_append.track_number = 99

        audio_mock = MagicMock()
        audio_mock.tag = MagicMock()
        audio_mock.tag.version = (2, 4)
        audio_mock.save = Mock(return_value=None)
        when(shutil).copyfile(source_file_path, target_file_path).thenReturn(None)
        when(eyed3).load(target_file_path).thenReturn(audio_mock)
        # WHEN
        sut.copy_audio(
            source_file_path,
            target_file_path,
            tags_to_append,
        )

        # THEN

    def test_copy_audio_when_target_file_has_no_tags(
        self,
        sut: AudioFileManagerInterface,
        when,
    ):
        # GIVEN
        source_file_path = os.path.join("source_root", "01", "01.mp3")
        target_file_path = os.path.join("target_root", "01", "01.mp3")
        tags_to_append = TagCollection()
        tags_to_append.artist = "artist_test"
        tags_to_append.title = "title_test"
        tags_to_append.album = "album_test"
        tags_to_append.track_number = 99

        audio_mock = MagicMock()
        audio_mock.save = Mock(return_value=None)
        when(shutil).copyfile(source_file_path, target_file_path).thenReturn(None)
        when(eyed3).load(target_file_path).thenReturn(audio_mock)
        # WHEN
        sut.copy_audio(
            source_file_path,
            target_file_path,
            tags_to_append,
        )

        # THEN

    # @pytest.mark.skip(reason="https://github.com/pytest-dev/pyfakefs/issues/1105")
    @e2e
    def test_copy_audio_with_fs(
        self,
        sut: AudioFileManagerInterface,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        source_file_path = os.path.join(test_assets_fs.test_assets_path, "0001.mp3")
        target_file_path = os.path.join(
            test_assets_fs.test_assets_path,
            "target_repo",
            "9999.mp3",
        )
        os.makedirs(
            os.path.join(test_assets_fs.test_assets_path, "target_repo"),
        )

        print(f"source_file_path: {os.listdir(os.path.dirname(source_file_path))}")
        tags_to_append = TagCollection()
        tags_to_append.artist = "artist_test"
        tags_to_append.title = "title_test"
        tags_to_append.album = "album_test"
        tags_to_append.track_number = 99

        # WHEN
        sut.copy_audio(
            source_file_path,
            target_file_path,
            tags_to_append,
        )

        # THEN
        sut_result = sut.read_id3_tags(target_file_path)
        assert sut_result.title == "title_test"
        assert sut_result.artist == "artist_test"
        assert sut_result.album == "album_test"
        assert sut_result.track_number == 99
