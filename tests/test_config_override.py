import os

import pytest
from mockito import ANY

from src.config import yaml_config
from src.config.configuration import RepositoryConfig
from src.repository import config_override

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestConfigOverride:
    def test_get_config_overrides_returns_overrides(
        self,
        when,
    ):
        # GIVEN
        when(os.path).isdir(...).thenReturn(True)
        when(os.path).isfile(...).thenReturn(True)
        when(yaml_config).create_yaml_object(
            os.path.join("test", "01", ".dfplayer_card_manager"),
            ANY,
        ).thenReturn(
            RepositoryConfig(valid_subdir_pattern="test_subdirs"),
        )
        when(yaml_config).create_yaml_object(
            os.path.join("test", "02", ".dfplayer_card_manager"),
            ANY,
        ).thenReturn(
            RepositoryConfig(valid_subdir_files_pattern="test_files"),
        )
        # WHEN
        overrides = config_override.get_config_overrides(
            "test",
            ["01", "02"],
            ".dfplayer_card_manager",
        )
        # THEN
        assert overrides["01"].valid_subdir_pattern == "test_subdirs"
        assert overrides["02"].valid_subdir_files_pattern == "test_files"
