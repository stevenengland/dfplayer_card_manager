import os

import pytest
from mockito import mock

from src.config import yaml_config
from src.config.configuration import (
    Configuration,
    ProcessingConfig,
    RepositoryConfig,
)
from src.dfplayer_card_manager import DfPlayerCardManager
from src.mp3.audio_file_manager import AudioFileManager
from src.mp3.tag_collection import TagCollection
from src.repository import config_override, repository_finder
from src.repository.detection_source import DetectionSource
from src.repository.diff_modes import DiffMode
from src.repository.repository_element import RepositoryElement
from tests.factories.configuration_factory import (
    create_source_repo_config,
    create_source_repo_config_all_sources_tag,
    create_target_repo_config,
)
from tests.factories.repository_element_factory import create_repository_element

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def dfplayer_card_manager() -> DfPlayerCardManager:
    audio_file_manager_mock = mock(AudioFileManager, strict=False)
    configuration = Configuration()
    configuration.repository_source = create_source_repo_config()
    configuration.repository_target = create_target_repo_config()
    sut = DfPlayerCardManager(
        "source_root",
        "target_root",
        audio_file_manager_mock,
        configuration,
    )
    return sut  # noqa: WPS331


class TestConfigReading:
    def test_config_reading_succeeds(self, sut: DfPlayerCardManager, when):
        # GIVEN
        init_config = Configuration()
        init_config.repository_processing.diff_method = DiffMode.tags
        when(os.path).isfile(
            Configuration().repository_processing.overrides_file_name,
        ).thenReturn(True)
        when(yaml_config).create_yaml_object(...).thenReturn(init_config)
        # WHEN
        config = sut.read_config()
        # THEN
        assert config.repository_processing.diff_method == DiffMode.tags

    def test_config_reading_raises(self, sut: DfPlayerCardManager, when):
        # GIVEN
        when(os.path).isfile(
            Configuration().repository_processing.overrides_file_name,
        ).thenReturn(False)
        # WHEN
        with pytest.raises(FileNotFoundError):
            sut.read_config()


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
        assert sut.target_repo.elements[0].repo_root_dir == sut.target_repo_root_dir
        assert sut.target_repo.elements[0].dir == "01"
        assert sut.target_repo.elements[0].file_name == "01.mp3"
        assert sut.target_repo.elements[1].dir == "02"
        assert sut.target_repo.elements[1].file_name == "01.mp3"
        assert sut.source_repo.elements[0].repo_root_dir == sut.source_repo_root_dir
        assert sut.source_repo.elements[0].dir == "01"
        assert sut.source_repo.elements[0].file_name == "01.mp3"
        assert sut.source_repo.elements[1].dir == "03"
        assert sut.source_repo.elements[1].file_name == "01.mp3"


class TestConfigOverrides:
    def test_reading_config_overrides_succeeds(self, sut: DfPlayerCardManager, when):
        # GIVEN

        when(config_override).get_config_overrides(...).thenReturn(
            {
                "01": RepositoryConfig(valid_subdir_files_pattern="test"),
                "03": RepositoryConfig(valid_subdir_files_pattern="test2"),
            },
        )
        # WHEN
        overrides = sut.read_config_overrides()
        # THEN
        assert len(overrides) == 2
        assert overrides["01"].valid_subdir_files_pattern == "test"
        assert (
            overrides["01"].valid_subdir_pattern
            == sut.config.repository_source.valid_subdir_pattern
        )
        assert overrides["03"].valid_subdir_files_pattern == "test2"
        assert (
            overrides["03"].valid_subdir_pattern
            == sut.config.repository_source.valid_subdir_pattern
        )


class TestElementUpdate:

    @pytest.mark.parametrize(
        "element, expected_element, config_overrides, source_configuration, "
        "target_configuration, processing_configuration, emulate_read_tag, emulate_read_hash",  # noqa: WPS326
        [
            (
                create_repository_element(
                    RepositoryElement(
                        repo_root_dir="source_root",
                        dir="02",
                        file_name="01.mp3",
                    ),
                ),
                RepositoryElement(
                    artist="artist_test",
                    track_number=1,
                    dir_number=2,
                ),
                {},
                create_source_repo_config_all_sources_tag(
                    RepositoryConfig(
                        valid_subdir_pattern=r"^(\d{2})$",
                        valid_subdir_files_pattern=r"(\d{2}).mp3",
                        track_number_match=1,
                        track_number_source=DetectionSource.filename,
                        dir_number_match=1,
                    ),
                ),
                create_target_repo_config(),
                ProcessingConfig(diff_method=DiffMode.hash_and_tags),
                True,
                True,
            ),
        ],
    )
    def test_element_update_succeeds(  # noqa: WPS211, C901
        self,
        sut: DfPlayerCardManager,
        when,
        element: RepositoryElement,
        expected_element: RepositoryElement,
        config_overrides: dict[str, RepositoryConfig],
        source_configuration: RepositoryConfig,
        target_configuration: RepositoryConfig,
        processing_configuration: ProcessingConfig,
        emulate_read_tag: bool,
        emulate_read_hash: bool,
    ):
        # GIVEN
        config = Configuration()
        config.repository_source = source_configuration
        config.repository_target = target_configuration
        config.repository_processing = processing_configuration
        sut.config = config
        sut.config_overrides = config_overrides

        sample_tags = TagCollection(
            artist="artist_test",
            title="title_test",
            album="album_test",
            track_number=99,
        )
        if emulate_read_hash and emulate_read_tag:
            when(sut.audio_manager).read_audio_content_and_id3_tags(...).thenReturn(
                (b"test", sample_tags),
            )
        if emulate_read_tag and not emulate_read_hash:
            when(sut.audio_manager).read_id3_tags(...).thenReturn(
                sample_tags,
            )
        if not emulate_read_tag and emulate_read_hash:
            when(sut.audio_manager).read_audio_content(...).thenReturn(b"test")
        # WHEN
        sut.update_element(element)
        # THEN
        # Make a copy of all values of element, when the value for the same key in expected_element is None
        for copy_key in expected_element.__annotations__:
            if (
                getattr(expected_element, copy_key) is None
                or getattr(expected_element, copy_key) == ""
            ):
                setattr(expected_element, copy_key, getattr(element, copy_key))

        # Assert that every attribute of element is equal to the corresponding attribute of expected_element
        for assertion_key in expected_element.__annotations__:
            assert getattr(element, assertion_key) == getattr(
                expected_element,
                assertion_key,
            )
