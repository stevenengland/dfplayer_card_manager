# -*- coding: cp1252 -*-
import os
import platform
from io import BytesIO

from FATtools import Volume
from FATtools.FAT import Dirtable

from dfplayer_card_manager.fat import fat_device_mount
from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.fat.fat_sorter_interface import FatSorterInterface


class FatSorter(FatSorterInterface):
    def sort_fat_dir(self, root_dir: str | BytesIO) -> None:
        root = Volume.vopen(root_dir, "r+b")
        root.sort()
        Volume.vclose(root)

    def sort_fat_volume(self, root_dir: str | BytesIO) -> None:
        root: Dirtable = None
        if isinstance(root_dir, str):
            root_dir = root_dir.rstrip(os.sep)
        try:
            root = Volume.vopen(root_dir, "r+b")
        except Exception as exception:
            raise FatError(exception)
        else:
            for directory_entry in root.walk():
                dir_to_open = directory_entry[0].lstrip(".").lstrip("\\").lstrip("/")
                subdir: Dirtable = (
                    root if directory_entry[0] == "." else root.opendir(dir_to_open)
                )
                subdir.sort()
        finally:
            if root:
                Volume.vclose(root)

    def is_fat_volume_sorted(self, root_dir: str | BytesIO) -> bool:  # noqa: WPS231
        root: Dirtable = None
        if isinstance(root_dir, str):
            root_dir = root_dir.rstrip(os.sep)
            root_dir = self._resolve_needed_path(root_dir)
        try:
            root = Volume.vopen(root_dir, "r+b")
        except Exception as exception:
            raise FatError(exception)
        else:
            return self._check_sorted(root)
        finally:
            if root:
                Volume.vclose(root)

    def _check_sorted(self, root: Dirtable) -> bool:
        for directory_entry in root.walk():
            dir_to_open = directory_entry[0].lstrip(".").lstrip("\\").lstrip("/")
            subdir: Dirtable = (
                root if directory_entry[0] == "." else root.opendir(dir_to_open)
            )
            if not self._is_dir_sorted(subdir.listdir()):
                return False
        return True

    def _is_dir_sorted(self, dirs: list[str]) -> bool:
        sorted_dirs = sorted(dirs)
        for original, sorted_val in zip(dirs, sorted_dirs):
            if original != sorted_val:
                return False
        return True

    def _resolve_needed_path(self, root_dir: str) -> str:
        if platform.system() == "Linux" and not root_dir.startswith("/dev"):
            root_dir = fat_device_mount.get_dev_root_dir(root_dir)
            if not root_dir:
                raise FatError(
                    "You're trying to access a path that is (or has no correspondent) device (/dev/xxx).",
                )
        return root_dir
