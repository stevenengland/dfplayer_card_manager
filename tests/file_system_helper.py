from pathlib import PurePath

from pyfakefs.fake_filesystem import FakeFilesystem


class FakeFileSystemHelper:
    def __init__(
        self,
        test_assets_path: PurePath,
        file_system: FakeFilesystem,
        read_only: bool = True,
    ) -> None:
        self._test_assets_path = test_assets_path
        self._file_system = file_system
        self._file_system.add_real_directory(str(test_assets_path), read_only=read_only)

    @property
    def test_assets_path(self) -> PurePath:
        return self._test_assets_path

    @property
    def file_system(self) -> FakeFilesystem:
        return self._file_system
