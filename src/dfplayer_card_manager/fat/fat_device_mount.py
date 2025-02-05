import platform
import re
import subprocess

from dfplayer_card_manager.fat.fat_error import FatError

OS_MACOS = "Darwin"
OS_WIN = "Windows"
OS_LINUX = "Linux"


def get_mount_path(device_path: str) -> str:
    if platform.system() == OS_WIN:
        return device_path
    if platform.system() == OS_LINUX:
        return _get_mount_path_linux(device_path)
    if platform.system() == OS_MACOS:
        return _get_mount_path_linux(device_path)
    raise NotImplementedError(f"{platform.system()} is not supported")


def get_dev_root_dir(mount_path: str) -> str:
    if platform.system() == OS_WIN:
        return mount_path
    if platform.system() == OS_LINUX:
        return _get_dev_root_dir_linux(mount_path)
    if platform.system() == OS_MACOS:
        return _get_dev_root_dir_linux(mount_path)
    raise NotImplementedError(f"{platform.system()} is not supported")


def detect_device_path_and_mount_path(sd_card_path: str) -> tuple[str, str]:
    if platform.system() == OS_WIN:
        return _detect_device_path_and_mount_path_windows(sd_card_path)
    if platform.system() == OS_LINUX:
        return _detect_device_path_and_mount_path_linux(sd_card_path)
    if platform.system() == OS_MACOS:
        return _detect_device_path_and_mount_path_linux(sd_card_path)
    raise NotImplementedError(f"{platform.system()} is not supported")


def _detect_device_path_and_mount_path_windows(sd_card_path: str) -> tuple[str, str]:
    return get_dev_root_dir(sd_card_path), get_mount_path(sd_card_path)


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
    df_value = _find_df_column(mount_path, lines, -1, 0)
    if platform.system() == OS_MACOS:
        return _extract_macos_disk(df_value)
    return df_value


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
    device_path = device_path.rstrip("/")  # specific to linux, no os.sep meaningful
    for line in lines:
        parts = line.split()
        if parts and parts[col_in] == device_path:
            if col_out == -1:
                return parts[-1]
            return parts[col_out]
    return ""


def _extract_macos_disk(df_value: str) -> str:
    if df_value.startswith("/dev/disk"):
        return df_value
    pattern = re.compile("^[^:]+://([^/]+)/")
    match = pattern.match(df_value)
    if match:
        part = match.group(1)
        return f"/dev/{part}"
    return df_value
