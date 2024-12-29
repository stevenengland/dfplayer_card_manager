import os
import platform
import subprocess  # noqa: S404
from unittest.mock import MagicMock

import pytest

from dfplayer_card_manager.repository.fat_checker import check_is_fat32

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestFatCheckerUnix:
    def test_check_fat32_unix_exists_and_is_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(
            stdout="Filesystem     Type 1K-blocks  Used Available Use% Mounted on\n/dev/sda2      vfat    523244   336    522908   1% /boot/efi",  # noqa: E501
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
        )
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        is_fat32_filesystem = check_is_fat32("/mnt/sdcard")
        assert not is_fat32_filesystem


class TestFatCheckerWindows:
    def test_check_fat32_windows_exists_and_is_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(stdout="File System Name : FAT32")
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

        is_fat32_filesystem = check_is_fat32("E:\\")
        assert not is_fat32_filesystem

    def test_check_fat32_windows_exists_and_is_not_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Windows")
        when(os.path).exists(...).thenReturn(True)

        mock_subprocess_run = MagicMock(stdout="File System Name : NTFS")
        when(subprocess).run(...).thenReturn(mock_subprocess_run)

        is_fat32_filesystem = check_is_fat32("E:\\")
        assert not is_fat32_filesystem
