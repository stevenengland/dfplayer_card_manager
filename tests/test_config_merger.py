import pytest

from dfplayer_card_manager.config import config_merger
from dfplayer_card_manager.config.configuration import (
    ProcessingConfig,
    RepositoryConfig,
)
from dfplayer_card_manager.repository.diff_modes import DiffMode

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestConfigMerging:
    def test_source_repo_configs_get_merged(self):
        # GIVEN
        config: RepositoryConfig = RepositoryConfig()
        config.album_match = 1
        config.valid_subdir_pattern = "test_subdirs_original"
        config.valid_subdir_files_pattern = "test_files_original"

        overrides_1: RepositoryConfig = RepositoryConfig()
        overrides_1.valid_subdir_pattern = "override_subdirs_1"
        overrides_1.valid_subdir_files_pattern = "override_files_1"
        overrides_2: RepositoryConfig = RepositoryConfig()
        overrides_2.valid_subdir_pattern = "override_subdirs_2"
        # WHEN
        merged_config_1 = config_merger.merge_configs(
            config,
            overrides_1,
        )
        merged_config_2 = config_merger.merge_configs(
            config,
            overrides_2,
        )
        # THEN
        assert config.valid_subdir_pattern == "test_subdirs_original"
        assert config.valid_subdir_files_pattern == "test_files_original"

        assert merged_config_1.album_match == 1
        assert merged_config_1.valid_subdir_pattern == "override_subdirs_1"
        assert merged_config_1.valid_subdir_files_pattern == "override_files_1"

        assert merged_config_2.album_match == 1
        assert merged_config_2.valid_subdir_pattern == "override_subdirs_2"
        assert merged_config_2.valid_subdir_files_pattern == "test_files_original"

    def test_processing_config_get_merged(self):
        # GIVEN
        config = ProcessingConfig()
        config.diff_method = DiffMode.hash
        config.overrides_file_name = "original_file_name"

        overrides = ProcessingConfig()
        overrides.overrides_file_name = "override_file_name"

        # WHEN
        merged_config = config_merger.merge_configs(
            config,
            overrides,
        )
        # THEN
        assert merged_config.diff_method == DiffMode.hash
        assert merged_config.overrides_file_name == "override_file_name"
