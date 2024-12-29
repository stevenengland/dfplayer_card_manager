# -*- coding: cp1252 -*-
from io import BytesIO

from FATtools.Volume import vclose, vopen

from dfplayer_card_manager.fat.fat_sorter_interface import FatSorterInterface


class FatSorter(FatSorterInterface):
    def sort_fat_root(self, root_dir: str | BytesIO) -> None:
        root = vopen(root_dir, "r+b")
        root.sort()
        vclose(root)
