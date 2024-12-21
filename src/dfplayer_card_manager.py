import os

from src.config import config_checker
from src.config.config_merger import merge_configs
from src.config.configuration import Configuration, RepositoryConfig
from src.dfplayer_card_manager_interface import DfPlayerCardManagerInterface
from src.mp3.audio_file_manager_interface import AudioFileManagerInterface
from src.repository import (
    config_override,
    repository_element_updater,
    repository_finder,
)
from src.repository.detection_source import DetectionSource
from src.repository.diff_modes import DiffMode
from src.repository.repository import Repository
from src.repository.repository_element import RepositoryElement


class DfPlayerCardManager(DfPlayerCardManagerInterface):  # noqa: WPS214
    def __init__(
        self,
        source_repo_root_dir: str,
        target_repo_root_dir: str,
        config: Configuration,
        audio_manager: AudioFileManagerInterface,
    ):
        self._config = config
        self._config_overrides: dict[str, RepositoryConfig] = {}
        self._audio_manager = audio_manager
        self._source_repo: Repository = Repository()
        self._target_repo: Repository = Repository()
        self._source_repo_root_dir = source_repo_root_dir
        self._target_repo_root_dir = target_repo_root_dir

    @property
    def config(self):
        return self._config

    @property
    def source_repo_root_dir(self):
        return self._source_repo_root_dir

    @property
    def target_repo_root_dir(self):
        return self._target_repo_root_dir

    @property
    def source_repo(self):
        return self._source_repo

    @property
    def target_repo(self):
        return self._target_repo

    @property
    def config_overrides(self):
        return self._config_overrides

    @config_overrides.setter
    def config_overrides(self, overrides):
        self._config_overrides = overrides

    def init(self):
        self.init_repositories()
        self.read_config_overrides()
        config_checker.check_repository_config(self._config.repository_source)
        config_checker.check_repository_config(self._config.repository_target)

    def init_repositories(self) -> None:
        source_repository_tree = self.get_source_repository_tree()
        target_repository_tree = self.get_target_repository_tree()
        for source_subdirectory, source_file in source_repository_tree:
            element = RepositoryElement()
            element.repo_root_dir = self._source_repo_root_dir or ""
            element.dir = source_subdirectory
            element.file_name = source_file
            self._source_repo.elements.append(element)
        for target_subdirectory, target_file in target_repository_tree:
            element = RepositoryElement()
            element.repo_root_dir = self._target_repo_root_dir or ""
            element.dir = target_subdirectory
            element.file_name = target_file
            self._target_repo.elements.append(element)

    def read_config_overrides(self) -> None:
        if self._source_repo_root_dir is None:
            raise ValueError("Repository source root directory is not set")
        self._config_overrides = config_override.get_config_overrides(
            self._source_repo_root_dir,
            # get all distinct subdirs from the source repository
            [element.dir for element in self._source_repo.elements],
            self._config.repository_processing.overrides_file_name,
        )

    def get_target_repository_tree(self) -> list[tuple[str, str]]:
        if self._target_repo_root_dir is None:
            raise ValueError("Repository target root directory is not set")
        if self._config.repository_target.valid_subdir_pattern is None:
            raise ValueError("Repository target valid subdir pattern is not set")
        if self._config.repository_target.valid_subdir_files_pattern is None:
            raise ValueError("Repository target valid subdir files pattern is not set")
        return repository_finder.get_repository_tree(
            self._target_repo_root_dir,
            self._config.repository_target.valid_subdir_pattern,
            self._config.repository_target.valid_subdir_files_pattern,
        )

    def get_source_repository_tree(
        self,
    ) -> list[tuple[str, str]]:
        if self._source_repo_root_dir is None:
            raise ValueError("Repository source root directory is not set")
        if self._config.repository_source.valid_subdir_pattern is None:
            raise ValueError("Repository source valid subdir pattern is not set")
        if self._config.repository_source.valid_subdir_files_pattern is None:
            raise ValueError("Repository source valid subdir files pattern is not set")
        valid_subdir_files_pattern_overrides = {}
        for subdir, config in self._config_overrides.items():
            if not config.valid_subdir_files_pattern:
                continue
            valid_subdir_files_pattern_overrides[subdir] = (
                config.valid_subdir_files_pattern
            )
        return repository_finder.get_repository_tree(
            self._source_repo_root_dir,
            self._config.repository_source.valid_subdir_pattern,
            self._config.repository_source.valid_subdir_files_pattern,
            valid_subdir_files_pattern_overrides,
        )

    def update_element(self, element: RepositoryElement):  # noqa: WPS231
        if element.repo_root_dir == self._target_repo_root_dir:
            applied_config = self._config.repository_target
        elif element.repo_root_dir == self._source_repo_root_dir:
            applied_config = self._get_applied_config(element)
        else:
            raise ValueError("The element does not belong to any of the repositories")

        is_tag_reading_needed = self.is_tag_reading_needed(applied_config)

        is_hash_reading_needed = self.is_hash_reading_needed(applied_config)

        if is_tag_reading_needed and is_hash_reading_needed:
            audio_content, id3_tags = (
                self._audio_manager.read_audio_content_and_id3_tags(
                    os.path.join(element.repo_root_dir, element.dir, element.file_name),
                )
            )
            repository_element_updater.update_element_by_tags(
                element,
                applied_config,
                id3_tags,
            )
            repository_element_updater.update_element_by_audio_content(
                element,
                audio_content,
            )
        elif is_tag_reading_needed and not is_hash_reading_needed:
            id3_tags = self._audio_manager.read_id3_tags(
                os.path.join(element.repo_root_dir, element.dir, element.file_name),
            )
            repository_element_updater.update_element_by_tags(
                element,
                applied_config,
                id3_tags,
            )
        elif not is_tag_reading_needed and is_hash_reading_needed:
            audio_content = self._audio_manager.read_audio_content(
                os.path.join(element.repo_root_dir, element.dir, element.file_name),
            )
            repository_element_updater.update_element_by_audio_content(
                element,
                audio_content,
            )

        return element

    def is_hash_reading_needed(self, applied_config) -> bool:
        return (
            self._config.repository_processing.diff_method == DiffMode.hash_and_tags
            or applied_config.diff_method == DiffMode.hash
        )

    def is_tag_reading_needed(self, applied_config) -> bool:
        return (
            self._config.repository_processing.diff_method  # noqa: WPS222
            == DiffMode.hash_and_tags
            or applied_config.diff_method == DiffMode.tags
            or applied_config.title_source == DetectionSource.tag
            or applied_config.artist_source == DetectionSource.tag
            or applied_config.album_source == DetectionSource.tag
            or applied_config.track_number_source == DetectionSource.tag
        )

    def _get_applied_config(self, element) -> RepositoryConfig:
        applied_config: RepositoryConfig = self._config.repository_source
        if element.dir in self._config_overrides:
            applied_config = merge_configs(
                self._config.repository_source,
                self._config_overrides.get(element.dir, RepositoryConfig()),
            )

        return applied_config
