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


class TestGetBlockDevice:
    def test_get_device_by_mount_path_succeeds(self, when, lsblk_mock):
        # GIVEN
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )

        # WHEN
        device_path = get_mount_path("/dev/sdb1")
        device_path_with_os_sep = get_mount_path("/dev/sdb1/")

        # THEN
        assert device_path == "/media/user/sdcard"
        assert device_path_with_os_sep == "/media/user/sdcard"

    def test_get_device_by_mount_path_fails(self, when, lsblk_mock):
        # GIVEN
        lsblk_mock.returncode = 1
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )

        with pytest.raises(FatError):
            get_mount_path("/dev/sdb1")


class TestGetMountPoint:

    def test_get_mount_point_by_device_path_succeeds(self, when, lsblk_mock):
        # GIVEN
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )

        # WHEN
        mount_path = get_dev_root_dir("/media/user/sdcard")
        mount_path_with_os_sep = get_dev_root_dir("/media/user/sdcard/")

        # THEN
        assert mount_path == "/dev/sdb1"
        assert mount_path_with_os_sep == "/dev/sdb1"

    def test_get_mount_point_by_device_path_fails(self, when, lsblk_mock):
        # GIVEN
        lsblk_mock.returncode = 1
        when(subprocess).run(["df", "-h"], ...).thenReturn(
            lsblk_mock,
        )

        with pytest.raises(FatError):
            get_dev_root_dir("/media/user/sdcard")
