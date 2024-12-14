import os
from unittest.mock import MagicMock

import eyed3
import pytest
from mockito import when

from src.mp3.audio_file_manager import AudioFileManager
from src.mp3.tag_collection import TagCollection
from src.mp3.tag_error import TagError
from tests.file_system_helper import FakeFileSystemHelper

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def tag_manager() -> AudioFileManager:
    sut = AudioFileManager()
    return sut  # noqa: WPS331


def test_read_id3_tags_with_valid_tags(sut: AudioFileManager):
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


def test_read_id3_tags_with_invalid_tags(sut: AudioFileManager):
    # GIVEN
    tag_mock = MagicMock()
    tag_mock.tag.version = (9,)

    when(eyed3).load(...).thenReturn(tag_mock)

    # WHEN
    # THEN
    with pytest.raises(expected_exception=TagError, match="Invalid"):
        sut.read_id3_tags("file_path")


@e2e
def test_read_id3_tags_from_file_wo_tags(
    sut: AudioFileManager,
    test_assets_fs: FakeFileSystemHelper,
):
    # GIVEN
    # WHEN
    # THEN
    with pytest.raises(expected_exception=TagError, match="Invalid"):
        sut.read_id3_tags(
            os.path.join(test_assets_fs.test_assets_path, "0003.mp3"),
        )


@e2e
def test_read_id3_tags_from_file_w_tags(
    sut: AudioFileManager,
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


@e2e
def test_read_audio_content(
    sut: AudioFileManager,
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
