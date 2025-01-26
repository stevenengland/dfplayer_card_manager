import os
import platform
import re
import subprocess  # noqa: S404

from dfplayer_card_manager.fat import fat_linux_mount
from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.os import path_sanitizer  # noqa: S404


def check_is_fat32(sd_card_path: str) -> bool:
    """Check if the SD card path exists and is fat32."""
    if platform.system() == "Windows":
        return _check_fat32_windows(sd_card_path)
    return _check_fat32_unix(sd_card_path)


def check_has_correct_allocation_unit_size(sd_card_path: str) -> bool:
    """Check if the SD card path has the correct allocation unit size."""
    if platform.system() == "Windows":
        return _check_allocation_unit_size_windows(sd_card_path)
    return _check_allocation_unit_size_unix(sd_card_path)


def _check_fat32_windows(sd_card_path: str) -> bool:
    sd_card_path = path_sanitizer.sanitize_windows_volume_path(sd_card_path)
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Volume -FilePath {sd_card_path} | Format-List FileSystemType",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return (
        subprocess_result.returncode == 0
        and "FileSystemType : FAT32" in subprocess_result.stdout
    )


def _check_fat32_unix(sd_card_path: str) -> bool:  # noqa: C901
    if not os.path.exists(  # Returns true for /dev/sda[1-9] and /mount/sdcard
        sd_card_path,
    ):
        return False

    subprocess_result = subprocess.run(
        ["lsblk", "-f"],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    if sd_card_path.startswith("/dev/"):
        sd_card_path = sd_card_path[5:]

    for line in subprocess_result.stdout.splitlines()[1:]:
        if re.match(f".*{sd_card_path}$", line) or re.match(
            f"^.*{sd_card_path} ",
            line,
        ):
            if "FAT32" in line:
                return True
    return False


def _check_allocation_unit_size_windows(sd_card_path: str) -> bool:
    sd_card_path = path_sanitizer.sanitize_windows_volume_path(sd_card_path)
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Volume -FilePath {sd_card_path} | Format-List AllocationUnitSize",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return "AllocationUnitSize : 32768" in subprocess_result.stdout


def _check_allocation_unit_size_unix(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    if sd_card_path.startswith("/dev/"):
        sd_card_path = fat_linux_mount.get_mount_path(sd_card_path)
        if not sd_card_path:
            raise FatError(f"Could not find mount point for {sd_card_path}")

    subprocess_result = subprocess.run(
        ["stat", sd_card_path],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return (
        subprocess_result.returncode == 0
        and "IO Block: 32768" in subprocess_result.stdout
    )
