import os

import pytest
from file_system_helper import FakeFileSystemHelper
from mockito import verify

from dfplayer_card_manager.repository.dfplayer_card_checker import (
    DfPlayerCardChecker,
)

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def sd_card_cleaner() -> DfPlayerCardChecker:
    sut = DfPlayerCardChecker()
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

    @e2e
    def test_delete_unwanted_root_dir_entries_on_real_fs(
        self,
        sut: DfPlayerCardChecker,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        sd_root_path = str(test_assets_fs.test_assets_path / "sdcard")
        test_assets_fs.file_system.create_dir(
            sd_root_path,
        )
        test_assets_fs.file_system.create_file(f"{sd_root_path}/01.file")
        test_assets_fs.file_system.create_dir(f"{sd_root_path}/003")
        # WHEN
        sut.delete_unwanted_root_dir_entries(sd_root_path)
        # THEN
        assert not os.path.exists(f"{sd_root_path}/01.file")
        assert not os.path.exists(f"{sd_root_path}/003")

    @e2e
    def test_delete_unwanted_subdir_entries_on_real_fs(
        self,
        sut: DfPlayerCardChecker,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        sd_root_path = str(test_assets_fs.test_assets_path / "sdcard")
        test_assets_fs.file_system.create_dir(
            sd_root_path,
        )
        test_assets_fs.file_system.create_dir(f"{sd_root_path}/01")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/01/001.mp3")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/01/002.mp3")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/01/fail.mp3")
        test_assets_fs.file_system.create_dir(f"{sd_root_path}/02")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/02/001.mp3")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/02/002.mp3")
        test_assets_fs.file_system.create_file(f"{sd_root_path}/02/.test")
        # WHEN
        sut.delete_unwanted_subdir_entries(sd_root_path)
        # THEN
        assert os.path.exists(f"{sd_root_path}/01/001.mp3")
        assert os.path.exists(f"{sd_root_path}/01/002.mp3")
        assert os.path.exists(f"{sd_root_path}/02/001.mp3")
        assert os.path.exists(f"{sd_root_path}/02/002.mp3")
        assert not os.path.exists(f"{sd_root_path}/01/fail.mp3")
        assert not os.path.exists(f"{sd_root_path}/02/.test")

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

    def test_get_subdir_numbering_gaps(self, sut, when):
        # GIVEN
        sd_root_path = "/sdcard"
        when(os).listdir(sd_root_path).thenReturn(
            [
                "01",
                "02",
            ],
        )
        when(os).listdir(os.path.join(sd_root_path, "01")).thenReturn(
            [
                "001",
                "002",
                "004",
                "005",
            ],
        )
        when(os).listdir(os.path.join(sd_root_path, "02")).thenReturn(
            [
                "001",
                "003",
                "006",
            ],
        )
        # WHEN
        gaps = sut.get_subdir_numbering_gaps(sd_root_path)
        # THEN
        assert gaps == [
            (1, 3),
            (2, 2),
            (2, 4),
            (2, 5),
        ]
