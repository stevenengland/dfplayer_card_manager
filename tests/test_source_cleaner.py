import os

import pytest

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
