import os

import pytest

from src.config.configuration import RepositorySourceConfig
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
        config = RepositorySourceConfig().from_yaml(config_path)  # type: ignore [no-untyped-call]

        # THEN
        assert config.root_dir == "/test/test_assets"
