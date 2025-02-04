import os
import platform
import re
import struct
import subprocess  # noqa: S404

from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.os import path_sanitizer  # noqa: S404


def check_is_fat32(sd_card_path: str) -> bool:
    """Check if the SD card path exists and is fat32."""
    if platform.system() == "Windows":
        return _check_fat32_windows(sd_card_path)
    elif platform.system() == "Linux":
        return _check_fat32_unix(sd_card_path)
    elif platform.system() == "Darwin":
        return _check_fat32_macos(sd_card_path)
    raise NotImplementedError(f"{platform.system()} is not supported")


def check_has_correct_allocation_unit_size(sd_card_path: str) -> bool:
    """Check if the SD card path has the correct allocation unit size."""
    if platform.system() == "Windows":
        return _check_allocation_unit_size_windows(sd_card_path)
    elif platform.system() == "Linux":
        return _check_allocation_unit_size_unix(sd_card_path)
    elif platform.system() == "Darwin":
        return _check_allocation_unit_size_macos(sd_card_path)
    raise NotImplementedError(f"{platform.system()} is not supported")


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


def _check_fat32_macos(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(
        ["diskutil", "info", "-plist", sd_card_path],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return (
        re.search(r"\<string\>.*FAT32\<\/string\>", subprocess_result.stdout)
        is not None
    )


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

    # root method on device path
    if sd_card_path.startswith("/dev/"):
        return (
            _get_allocation_unit_size_from_boot_sector(sd_card_path)
            == 32768  # noqa: WPS432
        )

    # non root method on mount path
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


def _check_allocation_unit_size_macos(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    # root method on device path
    if sd_card_path.startswith("/dev/"):
        return (
            _get_allocation_unit_size_from_boot_sector(sd_card_path)
            == 32768  # noqa: WPS432
        )

    # non root method on mount path
    subprocess_result = subprocess.run(
        ["stat", "-s", sd_card_path],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    return (
        subprocess_result.returncode == 0
        and "st_size=32768" in subprocess_result.stdout
    )


def _get_allocation_unit_size_from_boot_sector(device_path: str) -> int:
    # be sure to only use this function with eleveted priviliges
    with open(device_path, "rb") as device:
        # Read the first 512 bytes (boot sector)
        boot_sector = device.read(512)  # noqa: WPS432

        # Bytes 11-12: Bytes per sector (2 bytes, little-endian)
        bytes_per_sector = struct.unpack_from("<H", boot_sector, 11)[0]  # noqa: WPS432

        # Byte 13: Sectors per cluster (1 byte)
        sectors_per_cluster = struct.unpack_from("<B", boot_sector, 13)[  # noqa: WPS432
            0
        ]

        # Calculate allocation unit size (bytes per cluster)
        return bytes_per_sector * sectors_per_cluster
