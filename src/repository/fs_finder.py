import os
import re


def get_valid_root_dirs(
    root_dir: str,
    valid_dir_pattern: str = "",
) -> list[str]:
    subdirs = [
        entry
        for entry in os.listdir(root_dir)
        if re.match(valid_dir_pattern, entry)
        and os.path.isdir(os.path.join(root_dir, entry))  # noqa: WPS221
    ]
    subdirs.sort()
    return subdirs


def get_valid_subdir_files(
    subdir: str,
    valid_file_pattern: str = "",
) -> list[str]:
    valid_files = [
        entry
        for entry in os.listdir(subdir)
        if re.match(valid_file_pattern, entry)
        and os.path.isfile(os.path.join(subdir, entry))  # noqa: WPS221
    ]
    valid_files.sort()
    return valid_files
