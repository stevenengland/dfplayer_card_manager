import os
import platform
import subprocess

from dfplayer_card_manager.fat.fat_error import FatError


def get_mount_path(device_path: str) -> str:
    if platform.system() == "Windows":
        return device_path
    if platform.system() == "Linux":
        return _get_mount_path_linux(device_path)
    if platform.system() == "Darwin":
        raise NotImplementedError("macOS is not supported")
    raise NotImplementedError(f"{platform.system()} is not supported")


def get_dev_root_dir(mount_path: str) -> str:
    if platform.system() == "Windows":
        return mount_path
    if platform.system() == "Linux":
        return _get_dev_root_dir_linux(mount_path)
    if platform.system() == "Darwin":
        raise NotImplementedError("macOS is not supported")
    raise NotImplementedError(f"{platform.system()} is not supported")


def detect_device_path_and_mount_path(sd_card_path: str) -> tuple[str, str]:
    if platform.system() == "Windows":
        return _detect_device_path_and_mount_path_windows(sd_card_path)
    if platform.system() == "Linux":
        return _detect_device_path_and_mount_path_linux(sd_card_path)
    if platform.system() == "Darwin":
        raise NotImplementedError("macOS is not supported")
    raise NotImplementedError(f"{platform.system()} is not supported")


def _detect_device_path_and_mount_path_windows(sd_card_path: str) -> tuple[str, str]:
    return sd_card_path, sd_card_path


def _detect_device_path_and_mount_path_linux(sd_card_path: str) -> tuple[str, str]:
    if sd_card_path.startswith("/dev"):
        device_path = sd_card_path
        mountpoint_path = get_mount_path(sd_card_path)
    else:
        device_path = get_dev_root_dir(sd_card_path)
        mountpoint_path = sd_card_path

    return device_path, mountpoint_path


def _get_dev_root_dir_linux(mount_path: str) -> str:
    subprocess_result = subprocess.run(
        [
            "df",
            "-h",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    lines = subprocess_result.stdout.splitlines()
    return _find_df_column(mount_path, lines, -1, 0)


def _get_mount_path_linux(device_path: str) -> str:
    subprocess_result = subprocess.run(
        [
            "df",
            "-h",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    if subprocess_result.returncode != 0:
        raise FatError(subprocess_result.stderr)

    lines = subprocess_result.stdout.splitlines()
    return _find_df_column(device_path, lines, 0, -1)


def _find_df_column(
    device_path: str,
    lines: list[str],
    col_in: int,
    col_out: int,
) -> str:
    device_path = device_path.rstrip(os.sep)
    for line in lines:
        parts = line.split()
        if parts and parts[col_in] == device_path:
            if col_out == -1:
                return parts[-1]
            return parts[col_out]
    return ""
