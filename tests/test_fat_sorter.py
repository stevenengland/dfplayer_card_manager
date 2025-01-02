import io

import pytest
from FATtools.FAT import Dirtable
from FATtools.mkfat import exfat_mkfs, fat_mkfs
from FATtools.Volume import vclose, vopen

from dfplayer_card_manager.fat.fat_sorter import FatSorter

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def fat_sorter() -> FatSorter:
    sut = FatSorter()
    return sut  # noqa: WPS331


class TestFatSorter:
    @e2e
    def test_sort_fat_root(self, sut: FatSorter):
        # GIVEN
        bio = io.BytesIO((8 << 20) * b"\x00")
        # Reopen and format with EXFAT
        try:
            bio_disk = vopen(bio, "r+b", what="disk")
            print("Formatting...")
            exfat_mkfs(bio_disk, bio_disk.size)
        finally:
            vclose(bio_disk)

        # Reopen and create files
        try:
            bio_disk = vopen(bio, "r+b")
            file_ids = ("c", "a", "b", "d")
            for file_id in file_ids:
                text_file = bio_disk.create(f"{file_id}.txt")
                text_file.close()
        finally:
            vclose(bio_disk)
        # WHEN
        sut.sort_fat_dir(bio)
        try:
            bio_disk = vopen(bio, "r+b")
            sorted_entries = ["a.txt", "b.txt", "c.txt", "d.txt"]
            entries = bio_disk.listdir()
        finally:
            vclose(bio_disk)
        # THEN
        assert entries == sorted_entries


class TestFatNeedsSorting:
    @e2e
    def test_is_fat_volume_sorted(self, sut: FatSorter, when):  # noqa: WPS231
        # GIVEN
        bio = io.BytesIO((8 << 20) * b"\x00")
        # Reopen and format with EXFAT
        try:
            bio_disk = vopen(bio, "r+b", what="disk")
            print("Formatting...")
            fat_mkfs(bio_disk, bio_disk.size)
        finally:
            vclose(bio_disk)

        # Reopen and create files
        try:
            bio_root_dirtable: Dirtable = vopen(bio, "r+b")
            bio_root_dirtable.create("f01").close()
            bio_root_dirtable.create("f04").close()
            bio_root_dirtable.mkdir("d01").close()
            bio_root_dirtable.mkdir("d04").close()
            bio_root_dirtable.create(
                "d02_as_file",
            ).close()  # File with a directory name in between dirs
            bio_do04_dirtable = bio_root_dirtable.opendir("d04")
            bio_do04_dirtable.create("f41").close()
            bio_do04_dirtable.create("f43").close()
            bio_do04_dirtable.create("f42").close()
            bio_do04_dirtable.mkdir("d42").close()
            bio_root_dirtable.create("f02").close()
            bio_root_dirtable.create("f03").close()
            bio_root_dirtable.mkdir("d03").close()
        finally:
            vclose(bio_do04_dirtable)
            vclose(bio_root_dirtable)

        # WHEN
        is_sorted_before = sut.is_fat_volume_sorted(bio)
        sut.sort_fat_volume(bio)
        is_sorted_after = sut.is_fat_volume_sorted(bio)

        # THEN
        assert not is_sorted_before
        assert is_sorted_after

    def test_is_fat_root_sorted2(self, sut: FatSorter, when):  # noqa: WPS231
        sut.is_fat_volume_sorted("E:\\")
