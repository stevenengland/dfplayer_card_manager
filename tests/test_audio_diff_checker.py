import os

import pytest
from mockito import mock

from dfplayer_card_manager.mp3.audio_diff_checker import AudioDiffChecker
from dfplayer_card_manager.mp3.audio_file_manager import (
    AudioFileManager,
    AudioFileManagerInterface,
)
from dfplayer_card_manager.mp3.tag_collection import TagCollection

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def audio_diff_checker() -> AudioDiffChecker:
    audio_file_manager_mock = mock(AudioFileManagerInterface, strict=False)
    sut = AudioDiffChecker(audio_file_manager=audio_file_manager_mock)
    return sut  # noqa: WPS331


@pytest.fixture(scope="function", name="sute2e")
def audio_diff_checker_e2e() -> AudioDiffChecker:
    audio_file_manager = AudioFileManager()
    sut = AudioDiffChecker(audio_file_manager)
    return sut  # noqa: WPS331


class TestAudioDiffChecker:
    def test_check_diff_by_tags_succeeds(
        self,
        sut: AudioDiffChecker,
        when,
    ):
        # GIVEN
        audio_dir_path = "/audio_file"
        tags_target = TagCollection()
        tags_target.artist = "artist_test"
        tags_source = TagCollection()
        tags_source.artist = "artist_test"

        when(sut.audio_file_manager).read_id3_tags(audio_dir_path).thenReturn(
            tags_target,
        )
        # WHEN
        audio_diff_check_result = sut.check_diff_by_tags(audio_dir_path, tags_source)
        # THEN
        assert audio_diff_check_result

    def test_check_diff_by_tags_fails(
        self,
        sut: AudioDiffChecker,
        when,
    ):
        # GIVEN
        audio_dir_path = "/audio_file"
        tags_target = TagCollection()
        tags_target.artist = "artist_test1"
        tags_source = TagCollection()
        tags_source.artist = "artist_test2"

        when(sut.audio_file_manager).read_id3_tags(audio_dir_path).thenReturn(
            tags_target,
        )
        # WHEN
        audio_diff_check_result = sut.check_diff_by_tags(audio_dir_path, tags_source)
        # THEN
        assert not audio_diff_check_result

    @e2e
    def test_check_diff_by_hash_succeeds(
        self,
        sute2e: AudioDiffChecker,
        test_assets_tmp,
    ):
        # GIVEN
        audio_file_path = os.path.join(test_assets_tmp, "0001.mp3")
        audio_file_path_compare = os.path.join(
            test_assets_tmp,
            "0002.mp3",
        )
        # WHEN
        audio_diff_check_result = sute2e.check_diff_by_hash(
            audio_file_path,
            audio_file_path_compare,
        )
        # THEN
        assert audio_diff_check_result
