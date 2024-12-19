import pytest

from src.config import config_merger
from src.config.configuration import RepositoryConfig

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestConfigMerging:
    def test_source_repo_configs_get_merged(self):
        # GIVEN
        config: RepositoryConfig = RepositoryConfig()
        config.album_match = 1
        config.valid_subdir_pattern = "test_subdirs"
        config.valid_subdir_files_pattern = "test_files"

        overrides: RepositoryConfig = RepositoryConfig()
        overrides.valid_subdir_pattern = "override_subdirs"
        # WHEN
        merged_config = config_merger.merge_configs(
            config,
            overrides,
        )
        # THEN
        assert merged_config.album_match == 1
        assert merged_config.valid_subdir_pattern == "override_subdirs"
        assert merged_config.valid_subdir_files_pattern == "test_files"
