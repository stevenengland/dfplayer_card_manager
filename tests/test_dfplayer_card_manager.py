import pytest
from mockito import mock

from src.config.configuration import Configuration, RepositoryConfig
from src.dfplayer_card_manager import DfPlayerCardManager
from src.mp3.audio_file_manager import AudioFileManager
from src.repository import config_override, repository_finder
from tests.factories.configuration_factory import (
    create_source_repo_config,
    create_target_repo_config,
)

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def dfplayer_card_manager() -> DfPlayerCardManager:
    audio_file_manager_mock = mock(AudioFileManager, strict=False)
    configuration = Configuration()
    configuration.repository_source = create_source_repo_config()
    configuration.repository_target = create_target_repo_config()
    sut = DfPlayerCardManager(configuration, audio_file_manager_mock)
    return sut  # noqa: WPS331


class TestRepositoryTreeCreation:
    def test_target_tree_creation_succeeds(self, sut: DfPlayerCardManager, when):
        # GIVEN
        when(repository_finder).get_repository_tree(...).thenReturn(
            [
                ("01", "01.mp3"),
                ("02", "01.mp3"),
            ],
        )
        # WHEN
        target_tree = sut.get_target_repository_tree()
        # THEN
        assert target_tree == [
            ("01", "01.mp3"),
            ("02", "01.mp3"),
        ]

    def test_source_tree_creation_succeeds(self, sut: DfPlayerCardManager, when):
        # GIVEN
        sut.config_overrides = {
            "01": RepositoryConfig(valid_subdir_files_pattern="01.mp3"),
            "03": RepositoryConfig(valid_subdir_files_pattern="01.mp3"),
            "04": RepositoryConfig(valid_subdir_files_pattern=None),
        }
        when(repository_finder).get_repository_tree(
            any,
            any,
            any,
            {
                "01": "01.mp3",
                "03": "01.mp3",
            },
        ).thenReturn(
            [
                ("01", "01.mp3"),
                ("02", "01.mp3"),
            ],
        )
        # WHEN
        source_tree = sut.get_source_repository_tree()
        # THEN
        assert source_tree == [
            ("01", "01.mp3"),
            ("02", "01.mp3"),
        ]


class TestRepoInit:
    def test_repo_init_succeeds(self, sut: DfPlayerCardManager, when):
        # GIVEN
        when(sut).get_target_repository_tree().thenReturn(
            [
                ("01", "01.mp3"),
                ("02", "01.mp3"),
            ],
        )
        when(sut).get_source_repository_tree().thenReturn(
            [
                ("01", "01.mp3"),
                ("03", "01.mp3"),
            ],
        )
        # WHEN
        sut.init_repositories()
        # THEN
        assert (
            sut.target_repo.elements[0].repo_root_dir
            == sut.config.repository_target.root_dir
        )
        assert sut.target_repo.elements[0].dir == "01"
        assert sut.target_repo.elements[0].file_name == "01.mp3"
        assert sut.target_repo.elements[1].dir == "02"
        assert sut.target_repo.elements[1].file_name == "01.mp3"
        assert (
            sut.source_repo.elements[0].repo_root_dir
            == sut.config.repository_source.root_dir
        )
        assert sut.source_repo.elements[0].dir == "01"
        assert sut.source_repo.elements[0].file_name == "01.mp3"
        assert sut.source_repo.elements[1].dir == "03"
        assert sut.source_repo.elements[1].file_name == "01.mp3"


class TestConfigOverrides:
    def test_reading_config_overrides_succeeds(self, sut: DfPlayerCardManager, when):
        # GIVEN

        when(config_override).get_config_overrides(...).thenReturn(
            {
                "01": mock(RepositoryConfig),
                "03": mock(RepositoryConfig),
            },
        )
        # WHEN
        sut.read_config_overrides()
        # THEN
        assert len(sut.config_overrides) == 2
