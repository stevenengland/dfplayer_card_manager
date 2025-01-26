import os
import subprocess

from dfplayer_card_manager.fat.fat_error import FatError


def get_mount_path(device_path: str) -> str:
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


def get_dev_root_dir(mount_path: str) -> str:
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
