import os
import platform
import subprocess  # noqa: S404


def check_is_fat32(sd_card_path: str) -> bool:
    """Check if the SD card path exists and is fat32."""
    if platform.system() == "Windows":
        return _check_fat32_windows(sd_card_path)
    return _check_fat32_unix(sd_card_path)


def _check_fat32_windows(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(  # noqa: S607
        ["fsutil", "fsinfo", "volumeinfo", sd_card_path],
        capture_output=True,
        text=True,
        check=True,
        shell=False,  # noqa: S603
    )

    return "File System Name : FAT32" in subprocess_result.stdout


def _check_fat32_unix(sd_card_path: str) -> bool:
    if not os.path.exists(sd_card_path):
        return False

    subprocess_result = subprocess.run(  # noqa: S607
        ["df", "-T", sd_card_path],
        capture_output=True,
        text=True,
        check=True,
        shell=False,  # noqa: S603
    )

    lines = subprocess_result.stdout.split("\n")
    second_line = lines[1]
    columns = second_line.split()
    fs_type = columns[1].lower()
    return fs_type in {"vfat", "fat32", "msdos"}
