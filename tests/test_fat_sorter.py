import io

import pytest
from FATtools.mkfat import exfat_mkfs
from FATtools.Volume import vclose, vopen

from dfplayer_card_manager.repository.fat_sorter import FatSorter

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def fat_sorter() -> FatSorter:
    sut = FatSorter()
    return sut  # noqa: WPS331


class TestFatSorter:
    @e2e
    def test_sort_fat_root(self, sut, when):
        # GIVEN
        bio = io.BytesIO((8 << 20) * b"\x00")
        # Reopen and format with EXFAT
        bio_disk = vopen(bio, "r+b", what="disk")
        print("Formatting...")
        exfat_mkfs(bio_disk, bio_disk.size)
        vclose(bio_disk)

        print("Writing...")
        bio_disk = vopen(bio, "r+b")
        file_ids = ("c", "a", "b", "d")
        for file_id in file_ids:
            text_file = bio_disk.create(f"{file_id}.txt")
            text_file.close()
        vclose(bio_disk)
        # WHEN
        sut.sort_fat_root(bio)
        bio_disk = vopen(bio, "r+b")
        sorted_entries = ["a.txt", "b.txt", "c.txt", "d.txt"]
        entries = bio_disk.listdir()
        # THEN
        assert entries == sorted_entries
