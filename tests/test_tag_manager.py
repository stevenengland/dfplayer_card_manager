from unittest.mock import MagicMock

import eyed3
import pytest
from mockito import when

from src.mp3.eyed3_tag_manager import Eyed3TagManager
from src.mp3.tag_collection import TagCollection
from src.mp3.tag_error import TagError

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def tag_manager() -> Eyed3TagManager:
    sut = Eyed3TagManager()
    return sut  # noqa: WPS331


def test_read_id3_tags_with_valid_tags(sut: Eyed3TagManager):
    # GIVEN
    tag_mock = MagicMock()
    tag_mock.tag.version = (4,)
    tag_mock.tag.v2.title = "Song Title"
    tag_mock.tag.v2.artist = "Artist Name"
    tag_mock.tag.v2.album = "Album Name"
    tag_mock.tag.v2.track_num = (1,)
    when(eyed3).load(...).thenReturn(tag_mock)

    # WHEN
    sut_result = sut.read_id3_tags("file_path")

    # THEN
    assert isinstance(sut_result, TagCollection)
    assert sut_result.title == "Song Title"
    assert sut_result.artist == "Artist Name"
    assert sut_result.album == "Album Name"
    assert sut_result.track_number == 1


def test_read_id3_tags_with_invalid_tags(sut: Eyed3TagManager):
    # GIVEN
    tag_mock = MagicMock()
    tag_mock.tag.version = (9,)

    when(eyed3).load(...).thenReturn(tag_mock)

    # WHEN
    # THEN
    with pytest.raises(expected_exception=TagError, match="Invalid"):
        sut.read_id3_tags("file_path")
