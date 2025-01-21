import os

import pytest
from file_system_helper import FakeFileSystemHelper

from dfplayer_card_manager.config import config_reader, yaml_config
from dfplayer_card_manager.config.configuration import OverrideConfig
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

    def test_read_override_config_is_resilient_to_missing_parts(self, when):
        # GIVEN
        config_file = os.path.join(
            "tests",
            "test_assets",
            "config_override_missing_parts.yaml",
        )
        when(yaml_config).create_yaml_object(...).thenReturn(OverrideConfig())
        when(os.path).isfile(...).thenReturn(True)
        # WHEN
        empty_override = config_reader.read_override_config(config_file)
        # THEN
        assert empty_override.repository_source
        assert empty_override.repository_processing
