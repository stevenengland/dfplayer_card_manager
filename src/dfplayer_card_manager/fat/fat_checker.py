import os
import platform
import subprocess  # noqa: S404

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

    subprocess_result = subprocess.run(  # noqa: S607
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Volume -FilePath {sd_card_path} | Format-List FileSystemType",
        ],
        capture_output=True,
        text=True,
        shell=False,  # noqa: S603
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return (
        subprocess_result.returncode == 0
        and "FileSystemType : FAT32" in subprocess_result.stdout
    )


def _check_fat32_unix(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(  # noqa: S607
        ["df", "-T", sd_card_path],
        capture_output=True,
        text=True,
        shell=False,  # noqa: S603
    )

    lines = subprocess_result.stdout.split("\n")
    second_line = lines[1]
    columns = second_line.split()
    fs_type = columns[1].lower()

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return subprocess_result.returncode == 0 and fs_type == "fat32"  # ToDo: only FAT32?


def _check_allocation_unit_size_windows(sd_card_path: str) -> bool:
    sd_card_path = path_sanitizer.sanitize_windows_volume_path(sd_card_path)
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(  # noqa: S607
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Volume -FilePath {sd_card_path} | Format-List AllocationUnitSize",
        ],
        capture_output=True,
        text=True,
        shell=False,  # noqa: S603
    )

    return (
        subprocess_result.returncode == 0
        and "AllocationUnitSize : 32768" in subprocess_result.stdout
    )


def _check_allocation_unit_size_unix(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(  # noqa: S607
        ["stat", sd_card_path],
        capture_output=True,
        text=True,
        shell=False,  # noqa: S603
    )

    return (
        subprocess_result.returncode == 0
        and "IO Block: 32768" in subprocess_result.stdout
    )
