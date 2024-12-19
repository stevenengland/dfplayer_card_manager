import os

import pytest

from src.config.configuration import Configuration, RepositoryConfig
from src.config.yaml_config import create_yaml_object
from src.repository.detection_source import DetectionSource
from src.repository.diff_modes import DiffMode
from tests.file_system_helper import FakeFileSystemHelper

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestConfigLoadingYaml:
    def test_load_repository_source_config(self, test_assets_fs: FakeFileSystemHelper):
        # GIVEN
        config_path = os.path.join(
            test_assets_fs.test_assets_path,
            "config_source_repo.yaml",
        )

        # WHEN
        config: RepositoryConfig = create_yaml_object(config_path, RepositoryConfig)

        # THEN
        assert config.artist_source == DetectionSource.dirname

    def test_load_full_config(self, test_assets_fs: FakeFileSystemHelper):
        # GIVEN
        config_path = os.path.join(
            test_assets_fs.test_assets_path,
            "config_full.yaml",
        )

        # WHEN
        config: Configuration = create_yaml_object(config_path, Configuration)

        # THEN
        assert config.repository_processing.diff_method == DiffMode.hash_and_tags
