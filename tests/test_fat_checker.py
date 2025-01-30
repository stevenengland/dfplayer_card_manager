import builtins
import os
import platform
import subprocess  # noqa: S404
from unittest.mock import MagicMock

import pytest

from dfplayer_card_manager.fat.fat_checker import (
    check_has_correct_allocation_unit_size,
    check_is_fat32,
)

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")

mock_subprocess_run_linux = MagicMock(
    stdout="""  AME   FSTYPE  FSVER            LABEL    UUID             FSAVAIL FSUSE% MOUNTPOINTS
                sda
                ├─sda1
                ├─sda2 vfat    FAT32                    1A60-9999        505,9M  1%     /boot/efi
                └─sda3 ext4    1.0                      71c53cd8-0ab2    4,7G    70%    /
                sdb
                ├─sdb1 ext4    1.0                      71c53cd8-1111    4,7G    70%    /media/user/usb
                └─sdb2 vfat    FAT32           TOSHIBA  4C1C-9999        28,9G   0%     /media/user/sdcard""",
    returncode=0,
)


class TestFat32CheckerUnix:
    def test_check_fat32_unix_exists_and_is_fat32(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)

        when(subprocess).run(["lsblk", "-f"], ...).thenReturn(
            mock_subprocess_run_linux,
        )

        is_fat32_filesystem_partition = check_is_fat32("/dev/sdb2")
        is_fat32_filesystem_mountpoint = check_is_fat32("/media/user/sdcard")

        assert is_fat32_filesystem_mountpoint
        assert is_fat32_filesystem_partition

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

        when(subprocess).run(...).thenReturn(mock_subprocess_run_linux)

        is_fat32_filesystem_mountpoint = check_is_fat32("/")
        is_fat32_filesystem_partition = check_is_fat32("/dev/sda1")
        is_fat32_filesystem_partition_partial = check_is_fat32("/media/user/")
        assert not is_fat32_filesystem_mountpoint
        assert not is_fat32_filesystem_partition
        assert not is_fat32_filesystem_partition_partial


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
            returncode=0,
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
        when(subprocess).run(["stat", "/mnt/sdcard"], ...).thenReturn(
            mock_subprocess_run,
        )

        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "/mnt/sdcard",
        )
        assert has_correct_allocation_unit_size

    def test_check_allocation_unit_size_unix_exists_and_has_correct_allocation_unit_size_using_device_path(
        self,
        when,
    ):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(os.path).exists(...).thenReturn(True)
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file  # noqa: WPS609
        mock_file.read.return_value = (
            b"\xebX\x90MSDOS5.0\x00\x02@D\x06\x02\x00\x00\x00\x00\xf8\x00\x00?\x00\xff\x00?\x00\x00\x00"
            + b"\x81\xe5\x9b\x03\xde\x1c\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x06\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01)\x15T\x1cLNO NAME    FAT32   3\xc9\x8e"
            + b"\xd1\xbc\xf4{\x8e\xc1\x8e\xd9\xbd\x00|\x88V@\x88N\x02\x8aV@\xb4A\xbb\xaaU\xcd\x13r\x10\x81"
            + b"\xfbU\xaau\n\xf6\xc1\x01t\x05\xfeF\x02\xeb-\x8aV@\xb4\x08\xcd\x13s\x05\xb9\xff\xff\x8a\xf1"
            + b"f\x0f\xb6\xc6@f\x0f\xb6\xd1\x80\xe2?\xf7\xe2\x86\xcd\xc0\xed\x06Af\x0f\xb7\xc9f\xf7\xe1f"
            + b"\x89F\xf8\x83~\x16\x00u9\x83~*\x00w3f\x8bF\x1cf\x83\xc0\x0c\xbb\x00\x80\xb9\x01\x00\xe8,"
            + b"\x00\xe9\xa8\x03\xa1\xf8}\x80\xc4|\x8b\xf0\xac\x84\xc0t\x17<\xfft\t\xb4\x0e\xbb\x07\x00"
            + b"\xcd\x10\xeb\xee\xa1\xfa}\xeb\xe4\xa1}\x80\xeb\xdf\x98\xcd\x16\xcd\x19f`\x80~\x02\x00\x0f"
            + b"\x84 \x00fj\x00fP\x06Sfh\x10\x00\x01\x00\xb4B\x8aV@\x8b\xf4\xcd\x13fXfXfXfX\xeb3f;F\xf8r"
            + b"\x03\xf9\xeb*f3\xd2f\x0f\xb7N\x18f\xf7\xf1\xfe\xc2\x8a\xcaf\x8b\xd0f\xc1\xea\x10\xf7v\x1a"
            + b"\x86\xd6\x8aV@\x8a\xe8\xc0\xe4\x06\n\xcc\xb8\x01\x02\xcd\x13fa\x0f\x82t\xff\x81\xc3\x00\x02"
            + b"f@Iu\x94\xc3BOOTMGR    \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\r\nDisk error\xff\r\nPress any key to restart\r\n\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xac\x01\xb9\x01\x00\x00U\xaa"
        )

        when(builtins).open("/dev/sdb1", ...).thenReturn(mock_file)
        # WHEN
        has_correct_allocation_unit_size = check_has_correct_allocation_unit_size(
            "/dev/sdb1",
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
