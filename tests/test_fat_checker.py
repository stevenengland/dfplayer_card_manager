import os
import platform
import subprocess  # noqa: S404
from unittest.mock import MagicMock

import pytest

from dfplayer_card_manager.fat.fat_checker import (  # noqa: WPS450
    _sanitize_windows_path,
    check_has_correct_allocation_unit_size,
    check_is_fat32,
)

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestFat32CheckerUnix:
    def test_check_fat32_unix_exists_and_is_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="Filesystem     Type 1K-blocks  Used Available Use% Mounted on\n/dev/sda2      FAT32    523244   336    522908   1% /boot/efi",  # noqa: E501
            returncode=0,
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        is_fat32_filesystem = check_is_fat32("/mnt/sdcard")
        assert is_fat32_filesystem

    def test_check_fat32_unix_does_not_exist(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(False)

        is_fat32_filesystem = check_is_fat32("/mnt/sdcard")
        assert not is_fat32_filesystem

    def test_check_fat32_unix_exists_and_is_not_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="Filesystem     Type 1K-blocks  Used Available Use% Mounted on\n/dev/sda2      ext4    523244   336    522908   1% /boot/efi",  # noqa: E501
            returncode=0,
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        is_fat32_filesystem = check_is_fat32("/mnt/sdcard")
        assert not is_fat32_filesystem


class TestFat32CheckerWindows:
    def test_check_fat32_windows_exists_and_is_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="\n\nFileSystemType : FAT32",
            returncode=0,
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        is_fat32_filesystem = check_is_fat32("E:\\")
        assert is_fat32_filesystem

    def test_check_fat32_windows_does_not_exist(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(False)

        # WHEN
        is_fat32_filesystem = check_is_fat32("E:\\")
        # THEN
        assert not is_fat32_filesystem

    def test_check_fat32_windows_exists_and_is_not_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(stdout="File System Name : NTFS", returncode=0)
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        is_fat32_filesystem = check_is_fat32("E:\\")
        assert not is_fat32_filesystem


class TestAllocationUnitSizeDetectionWindows:
    def test_check_allocation_unit_size_windows_exists_and_has_correct_allocation_unit_size(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="\nAllocationUnitSize : 32768\n\n",
            returncode=0,
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "E:\\",
        )
        assert has_correct_allocation_unit_size

    def test_check_allocation_unit_size_windows_does_not_exist(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(False)

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "E:\\",
        )
        assert not has_correct_allocation_unit_size

    def test_check_allocation_unit_size_windows_exists_and_has_incorrect_allocation_unit_size(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="\nAllocationUnitSize : 16384\n\n",
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "E:\\",
        )
        assert not has_correct_allocation_unit_size


class TestAllocationUnitSizeDetectionUnix:
    def test_check_allocation_unit_size_unix_exists_and_has_correct_allocation_unit_size(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="  File: /media/administer/TOSHIBA/\n  Size: 32768     	Blocks: 64         IO Block: 32768  directory",  # noqa: E501
            returncode=0,
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "/mnt/sdcard",
        )
        assert has_correct_allocation_unit_size

    def test_check_allocation_unit_size_unix_does_not_exist(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(False)

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "/mnt/sdcard",
        )
        assert not has_correct_allocation_unit_size

    def test_check_allocation_unit_size_unix_exists_and_has_incorrect_allocation_unit_size(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="  File: /media/administer/TOSHIBA/\n  Size: 16384     	Blocks: 64         IO Block: 16384  directory",  # noqa: E501
            returncode=0,
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "/mnt/sdcard",
        )
        assert not has_correct_allocation_unit_size


class TestPathSanitation:
    @pytest.mark.parametrize(
        "path",
        [
            "E:",
            "E:\\",
        ],
    )
    def test_sanitize_windows_path(self, path):
        # GIVEN
        path = "E:\\"
        # WHEN
        sanitized_path = _sanitize_windows_path(path)
        # THEN
        assert sanitized_path == f"E:{os.sep}"
