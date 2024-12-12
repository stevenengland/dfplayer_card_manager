import os

import pytest
from mockito import verify

from src.repository.source_cleaner import SdCardCleaner

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def sd_card_cleaner() -> SdCardCleaner:
    sut = SdCardCleaner()
    return sut  # noqa: WPS331


class TestUnwantedDirs:
    def test_sd_root_dir_errors_are_reported(self, sut, when):
        # GIVEN
        sd_root_path = "/sdcard"
        when(os).listdir(sd_root_path).thenReturn(
            [
                "mp3",
                "advertisment",
                "01.file",  # error
                "02.dir",
                "003.dir",  # error
                "3.dir",  # error
                "5dir",  # error
                ".6dir",  # error
            ],
        )
        when(os.path).isfile(...).thenReturn(False)
        when(os.path).isfile("01.file").thenReturn(True)
        # WHEN
        errors = sut.get_unwanted_root_dir_entries(sd_root_path)
        # THEN
        assert errors == [
            "01.file",  # error
            "003.dir",  # error
            "3.dir",  # error
            "5dir",  # error
            ".6dir",  # error
        ]

    def test_delete_unwanted_root_dir_entries(self, sut, when):
        # GIVEN
        file_paths = [
            "/sdcard/01.file",
            "/sdcard/003.dir",
        ]

        when(os.path).isfile("/sdcard/01.file").thenReturn(True)

        when(os.path).isfile("/sdcard/003.dir").thenReturn(False)
        when(os).listdir("/sdcard/003.dir").thenReturn([])

        when(os).remove(...).thenReturn(None)
        when(os).rmdir(...).thenReturn(None)

        # WHEN
        sut.delete_unwanted_root_dir_entries(file_paths)

        # THEN
        verify(os).remove("/sdcard/01.file")
        verify(os).rmdir("/sdcard/003.dir")
