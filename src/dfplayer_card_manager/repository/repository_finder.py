import os
import re
from typing import Optional


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


def get_repository_tree(
    root_dir: str,
    valid_root_subdir_pattern: str,
    valid_subdir_files_pattern: str,
    valid_subdir_files_pattern_overrides: Optional[dict[str, str]] = None,
) -> list[tuple[str, str]]:
    if valid_subdir_files_pattern_overrides is None:
        valid_subdir_files_pattern_overrides = {}
    repository_tree = []
    # get valid root dirs
    valid_root_subdirs = get_valid_root_dirs(root_dir, valid_root_subdir_pattern)
    for valid_root_subdir in valid_root_subdirs:
        # get valid files in subdir
        valid_subdir = os.path.join(root_dir, valid_root_subdir)
        # if the valid subdir is listed in the overrides, use the override pattern
        if valid_root_subdir in valid_subdir_files_pattern_overrides:
            valid_subdir_files_pattern = valid_subdir_files_pattern_overrides.get(
                valid_root_subdir,
                valid_subdir_files_pattern,
            )
        valid_files = get_valid_subdir_files(valid_subdir, valid_subdir_files_pattern)
        for valid_file in valid_files:
            repository_tree.append((valid_root_subdir, valid_file))
    return repository_tree
