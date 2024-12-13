import os

import pytest
from mockito import verify

from src.repository.source_cleaner import SdCardCleaner
from tests.file_system_helper import FakeFileSystemHelper

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def sd_card_cleaner() -> SdCardCleaner:
    sut = SdCardCleaner()
    return sut  # noqa: WPS331


class TestUnwantedDirsAndFiles:
    def test_sd_root_dir_errors_are_reported(self, sut, when):
        # GIVEN
        sd_root_path = "/sdcard"
        when(os).listdir(sd_root_path).thenReturn(
            [
                "mp3",
                "advertisment",
                "01.file",  # error
                "02",
                "003",  # error
                "3",  # error
                ".6dir",  # error
                ".git",
            ],
        )
        when(os.path).isfile(...).thenReturn(False)
        when(os.path).isfile("01.file").thenReturn(True)
        # WHEN
        errors = sut.get_unwanted_root_dir_entries(sd_root_path)
        # THEN
        assert errors == [
            "01.file",  # error
            "003",  # error
            "3",  # error
            ".6dir",  # error
            ".git",
        ]

    @e2e
    def test_sd_root_dir_errors_are_reported_on_real_fs(
        self,
        sut,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        test_assets_fs.file_system.create_dir(
            test_assets_fs.test_assets_path / "sdcard",
        )
        sd_root_path = str(test_assets_fs.test_assets_path / "sdcard")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/01.file")
        test_assets_fs.file_system.create_dir(f"{sd_root_path}/003")
        test_assets_fs.file_system.create_dir(f"{sd_root_path}/.git")
        test_assets_fs.file_system.create_dir(f"{sd_root_path}/02")
        # WHEN
        errors = sut.get_unwanted_root_dir_entries(sd_root_path)
        # THEN
        assert errors == [
            "01.file",  # error
            "003",  # error
            ".git",
        ]

    def test_delete_unwanted_root_dir_entries(self, sut, when):
        # GIVEN
        file_paths = [
            "/sdcard/01.file",
            "/sdcard/003.dir",
        ]
        when(sut).get_unwanted_root_dir_entries(...).thenReturn(file_paths)
        when(os.path).isfile("/sdcard/01.file").thenReturn(True)

        when(os.path).isfile("/sdcard/003.dir").thenReturn(False)
        when(os).listdir("/sdcard/003.dir").thenReturn([])

        when(os).remove(...).thenReturn(None)
        when(os).rmdir(...).thenReturn(None)

        # WHEN
        sut.delete_unwanted_root_dir_entries("/sdcard")

        # THEN
        verify(os).remove("/sdcard/01.file")
        verify(os).rmdir("/sdcard/003.dir")

    def test_get_root_dir_numbering_gaps(self, sut, when):
        # GIVEN
        sd_root_path = "/sdcard"
        when(os).listdir(sd_root_path).thenReturn(
            [
                "01",
                "02",
                "004.dir",
                "03",
                "05",
                "09",
            ],
        )
        # WHEN
        gaps = sut.get_root_dir_numbering_gaps(sd_root_path)
        # THEN
        assert gaps == [4, 6, 7, 8]
