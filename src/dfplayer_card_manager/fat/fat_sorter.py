# -*- coding: cp1252 -*-
from io import BytesIO

from FATtools.FAT import Dirtable
from FATtools.Volume import vclose, vopen

from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.fat.fat_sorter_interface import FatSorterInterface


class FatSorter(FatSorterInterface):
    def sort_fat_dir(self, root_dir: str | BytesIO) -> None:
        root = vopen(root_dir, "r+b")
        root.sort()
        vclose(root)

    def sort_fat_volume(self, root_dir: str | BytesIO) -> None:
        try:
            root: Dirtable = vopen(root_dir, "r+b")
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
            vclose(root)

    def is_fat_root_sorted(self, root_dir: str | BytesIO) -> bool:
        try:
            root: Dirtable = vopen(root_dir, "r+b")
        except Exception as exception:
            raise FatError(exception)
        else:
            for directory_entry in root.walk():
                dir_to_open = directory_entry[0].lstrip(".").lstrip("\\").lstrip("/")
                subdir: Dirtable = (
                    root if directory_entry[0] == "." else root.opendir(dir_to_open)
                )
                if not self._is_dir_sorted(subdir.listdir()):
                    return False
        finally:
            vclose(root)
        return True

    def _is_dir_sorted(self, dirs: list[str]) -> bool:
        sorted_dirs = sorted(dirs)
        for original, sorted_val in zip(dirs, sorted_dirs):
            if original != sorted_val:
                return False
        return True
