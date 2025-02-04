import platform
import subprocess  # noqa: S404
from unittest.mock import MagicMock

import pytest

from dfplayer_card_manager.fat.fat_device_mount import (
    get_dev_root_dir,
    get_mount_path,
)
from dfplayer_card_manager.fat.fat_error import FatError

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="lsblk_mock")
def get_lsblk_mock():
    return MagicMock(
        stdout="""  Filesystem      Size  Used Avail Use% Mounted on
    tmpfs           198M  2,7M  195M   2% /run
    /dev/sda3        20G   15G  3,9G  79% /
    tmpfs           988M   60M  928M   7% /dev/shm
    tmpfs           5,0M  4,0K  5,0M   1% /run/lock
    /dev/sda2       512M  6,1M  506M   2% /boot/efi
    tmpfs           198M   76K  198M   1% /run/user/1000
    /dev/loop0      9,9M   512  9,9M   1% /home/user/usbtest/usbtestmount
    /dev/sdb1        29G  128K   29G   1% /media/user/sdcard""",
        returncode=0,
    )


@pytest.fixture(scope="function", name="df_mock_macos")
def get_df_mock_macos():
    return MagicMock(
        stdout="""Filesystem            Size   Used  Avail Capacity iused      ifree  iused  Mounted on
                /dev/disk1s4s1           80Gi  8.2Gi   61Gi    12%  348618  635160440    0%   /
                devfs                   196Ki  196Ki    0Bi   100%     678          0  100%   /dev
                /dev/disk1s2             80Gi  1.7Gi   61Gi     3%     913  635160440    0%   /System/Volumes/Preboot
                /dev/disk1s6             80Gi  1.0Gi   61Gi     2%       2  635160440    0%   /System/Volumes/VM
                /dev/disk1s5             80Gi  416Ki   61Gi     1%      20  635160440    0%   /System/Volumes/Update
                /dev/disk1s1             80Gi  7.2Gi   61Gi    11%  210908  635160440    0%   /System/Volumes/Data
                map auto_home             0Bi    0Bi    0Bi   100%       0          0  100%   /System/Volumes/Data/home
                /dev/disk2s0s2          3.2Mi  3.2Mi    0Bi   100%     108 4294967171    0%   /Volumes/VMware Tools
                /Users/sten/Downloads/   80Gi  6.2Gi   62Gi    10%  191780  646082480    0%   /private/var/folders/hh/9
                msdos://disk3s1/TOSHIBA  29Gi  224Ki   29Gi     1%       1          0  100%   /Volumes/TOSHIBA
                /dev/disk4               39Mi  1.5Ki   39Mi     1%       0          0  100%   /Volumes/dfplayer""",
        returncode=0,
    )


class TestGetBlockDevice:
    def test_get_device_by_mount_path_succeeds_linux(self, when, lsblk_mock):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )

        # WHEN
        device_path = get_mount_path("/dev/sdb1")
        device_path_with_os_sep = get_mount_path("/dev/sdb1/")

        # THEN
        assert device_path == "/media/user/sdcard"
        assert device_path_with_os_sep == "/media/user/sdcard"

    def test_get_device_by_mount_path_fails_linux(self, when, lsblk_mock):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        lsblk_mock.returncode = 1
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )
        # WHEN
        # THEN
        with pytest.raises(FatError):
            get_mount_path("/dev/sdb1")

    def test_get_device_by_mount_path_succeeds_macos(self, when, df_mock_macos):
        # GIVEN
        when(platform).system().thenReturn("Darwin")
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            df_mock_macos,
        )

        # WHEN
        device_path = get_mount_path("/dev/disk4")
        device_path_with_os_sep = get_mount_path("/dev/disk4/")

        # THEN
        assert device_path == "/Volumes/dfplayer"
        assert device_path_with_os_sep == "/Volumes/dfplayer"

    def test_get_device_by_mount_path_fails_macos(self, when, df_mock_macos):
        # GIVEN
        when(platform).system().thenReturn("Darwin")
        df_mock_macos.returncode = 1
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            df_mock_macos,
        )
        # WHEN
        # THEN
        with pytest.raises(FatError):
            get_mount_path("/dev/disk4")

    def test_get_device_by_mount_path_succeeds_windows(self, when, lsblk_mock):
        # GIVEN
        when(platform).system().thenReturn("Windows")

        # WHEN
        device_path = get_mount_path("tests/test_assets")
        # THEN
        assert device_path == "tests/test_assets"


class TestGetMountPoint:

    def test_get_mount_point_by_device_path_succeeds_linux(self, when, lsblk_mock):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )

        # WHEN
        mount_path = get_dev_root_dir("/media/user/sdcard")
        mount_path_with_os_sep = get_dev_root_dir("/media/user/sdcard/")

        # THEN
        assert mount_path == "/dev/sdb1"
        assert mount_path_with_os_sep == "/dev/sdb1"

    def test_get_mount_point_by_device_path_fails_linux(self, when, lsblk_mock):
        # GIVEN
        when(platform).system().thenReturn("Linux")
        lsblk_mock.returncode = 1
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )
        # WHEN
        # THEN

        with pytest.raises(FatError):
            get_dev_root_dir("/media/user/sdcard")

    def test_get_mount_point_by_device_path_succeeds_macos(self, when, df_mock_macos):
        # GIVEN
        when(platform).system().thenReturn("Darwin")
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            df_mock_macos,
        )

        # WHEN
        mount_path = get_dev_root_dir("/Volumes/dfplayer")
        mount_path_with_os_sep = get_dev_root_dir("/Volumes/dfplayer/")
        mount_path_with_os_macos_prefix = get_dev_root_dir("/Volumes/TOSHIBA")

        # THEN
        assert mount_path == "/dev/disk4"
        assert mount_path_with_os_sep == "/dev/disk4"
        assert mount_path_with_os_macos_prefix == "/dev/disk3s1"

    def test_get_mount_point_by_device_path_fails_macos(self, when, df_mock_macos):
        # GIVEN
        when(platform).system().thenReturn("Darwin")
        df_mock_macos.returncode = 1
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            df_mock_macos,
        )
        # WHEN
        # THEN

        with pytest.raises(FatError):
            get_dev_root_dir("/Volumes/TOSHIBA")

    def test_get_mount_point_by_device_path_succeeds_windows(self, when, lsblk_mock):
        # GIVEN
        when(platform).system().thenReturn("Windows")

        # WHEN
        mount_path = get_dev_root_dir("tests/test_assets")

        # THEN
        assert mount_path == "tests/test_assets"
