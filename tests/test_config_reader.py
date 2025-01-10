import os

import pytest
from file_system_helper import FakeFileSystemHelper

from dfplayer_card_manager.config import config_reader
from dfplayer_card_manager.repository.diff_modes import DiffMode

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestConfigReading:
    @e2e
    def test_read_config(self, test_assets_fs: FakeFileSystemHelper):
        # GIVEN
        config_file = os.path.join(
            test_assets_fs.test_assets_path,
            "config_override.yaml",
        )
        # WHEN
        config = config_reader.read_override_config(config_file)
        # THEN
        assert config.repository_source.album_match == 2
        assert config.repository_processing.diff_method == DiffMode.hash_and_tags

    def test_config_reading_raises(self):
        # GIVEN

        # WHEN
        # THEN
        with pytest.raises(FileNotFoundError):
            config_reader.read_override_config("non_existent_file")
