import os
from typing import Optional

from dfplayer_card_manager.config import config_checker, config_merger
from dfplayer_card_manager.config.configuration import (
    Configuration,
    RepositoryConfig,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_interface import (
    DfPlayerCardManagerInterface,
)
from dfplayer_card_manager.logging.logger_interface import LoggerInterface
from dfplayer_card_manager.mp3.audio_file_manager_interface import (
    AudioFileManagerInterface,
)
from dfplayer_card_manager.mp3.tag_collection import TagCollection
from dfplayer_card_manager.repository import (
    config_override,
    repository_comparator,
    repository_element_checker,
    repository_element_updater,
    repository_finder,
)
from dfplayer_card_manager.repository.compare_result import CompareResult
from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)
from dfplayer_card_manager.repository.detection_source import DetectionSource
from dfplayer_card_manager.repository.diff_modes import DiffMode
from dfplayer_card_manager.repository.repository import Repository
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


class DfPlayerCardManager(DfPlayerCardManagerInterface):  # noqa: WPS214

    def __init__(  # noqa: WPS211
        self,
        source_repo_root_dir: str,
        target_repo_root_dir: str,
        audio_manager: AudioFileManagerInterface,
        logger: LoggerInterface,
        config: Optional[Configuration] = None,
    ):
        self._config_overrides: dict[str, RepositoryConfig] = {}
        self._audio_manager = audio_manager
        self._source_repo: Repository = Repository()
        self._target_repo: Repository = Repository()
        self._source_repo_root_dir = source_repo_root_dir
        self._target_repo_root_dir = target_repo_root_dir
        self._logger = logger

        self._config: Configuration = config

    @property
    def audio_manager(self):
        return self._audio_manager

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def source_repo_root_dir(self):
        return self._source_repo_root_dir

    @source_repo_root_dir.setter
    def source_repo_root_dir(self, source_repo_root_dir):
        self._source_repo_root_dir = source_repo_root_dir

    @property
    def target_repo_root_dir(self):
        return self._target_repo_root_dir

    @target_repo_root_dir.setter
    def target_repo_root_dir(self, target_repo_root_dir):
        self._target_repo_root_dir = target_repo_root_dir

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

    # ToDo: tests
    def create_repositories(self) -> None:
        self._reset()
        if not os.path.isdir(self._source_repo_root_dir):
            raise ValueError("Source repository root directory is not a directory")
        if not os.path.isdir(self._target_repo_root_dir):
            raise ValueError("Target repository root directory is not a directory")

        config_checker.check_repository_config(self._config.repository_source)
        config_checker.check_repository_config(self._config.repository_target)
        self._config_overrides = self.read_config_overrides()
        for _subdir, config in self._config_overrides.items():
            config_checker.check_repository_config(config)
        self.init_repositories()
        self.complete_repositories()

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

    def complete_repositories(self) -> None:
        for source_repo_element in self._source_repo.elements:
            self.update_element(source_repo_element)
        for target_repo_element in self._target_repo.elements:
            self.update_element(target_repo_element)

    def read_config_overrides(self) -> dict[str, RepositoryConfig]:
        overrides = config_override.get_config_overrides(
            self._source_repo_root_dir,
            # get all distinct subdirs from the source repository
            [element.dir or "" for element in self._source_repo.elements],
            self._config.repository_processing.overrides_file_name,
        )
        for subdir, config in overrides.items():
            overrides[subdir] = config_merger.merge_configs(
                self._config.repository_source,
                config,
            )
        return overrides

    def get_target_repository_tree(self) -> list[tuple[str, str]]:
        if self._config.repository_target.valid_subdir_pattern is None:
            return []
        if self._config.repository_target.valid_subdir_files_pattern is None:
            return []
        return repository_finder.get_repository_tree(
            self._target_repo_root_dir,
            self._config.repository_target.valid_subdir_pattern,
            self._config.repository_target.valid_subdir_files_pattern,
        )

    def get_source_repository_tree(
        self,
    ) -> list[tuple[str, str]]:
        if self._config.repository_source.valid_subdir_pattern is None:
            return []
        if self._config.repository_source.valid_subdir_files_pattern is None:
            return []
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
        applied_config = self._get_applied_config(element)

        # Update portion without file reading
        repository_element_updater.update_element_by_dir(
            element=element,
            config=applied_config,
        )
        repository_element_updater.update_element_by_filename(
            element=element,
            config=applied_config,
        )

        # File reading portion of the update
        is_tag_reading_needed = self.is_tag_reading_needed(applied_config)

        is_hash_reading_needed = self.is_hash_reading_needed()

        element_full_path = os.path.join(
            element.repo_root_dir,
            element.dir,
            element.file_name,
        )

        if is_tag_reading_needed and is_hash_reading_needed:
            audio_content, id3_tags = (
                self._audio_manager.read_audio_content_and_id3_tags(
                    element_full_path,
                    self._target_repo_root_dir != element.repo_root_dir,
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
                element_full_path,
                self._target_repo_root_dir != element.repo_root_dir,
            )
            repository_element_updater.update_element_by_tags(
                element,
                applied_config,
                id3_tags,
            )
        elif not is_tag_reading_needed and is_hash_reading_needed:
            audio_content = self._audio_manager.read_audio_content(
                element_full_path,
            )
            repository_element_updater.update_element_by_audio_content(
                element,
                audio_content,
            )

        # Final check
        repository_element_checker.check_element(element)

    def is_hash_reading_needed(self) -> bool:
        return self._config.repository_processing.diff_method in {
            DiffMode.hash_and_tags,
            DiffMode.hash,
        }

    def is_tag_reading_needed(self, applied_config: RepositoryConfig) -> bool:
        return (
            applied_config.title_source == DetectionSource.tag  # noqa: WPS222
            or applied_config.artist_source == DetectionSource.tag
            or applied_config.album_source == DetectionSource.tag
            or applied_config.dir_number_source == DetectionSource.tag
            or applied_config.track_number_source == DetectionSource.tag
        )

    def get_repositories_comparison(
        self,
        stuff_missing_elements=False,
    ) -> list[CompareResult]:
        unstuffed_compare_results = repository_comparator.compare_repository_elements(
            self._source_repo.elements,
            self._target_repo.elements,
            self._config.repository_processing.diff_method or DiffMode.hash_and_tags,
        )

        if not stuff_missing_elements:
            return unstuffed_compare_results

        return repository_comparator.stuff_compare_results(
            unstuffed_compare_results,
        )

    # ToDo: Rewrite to use CompareElement
    def write_change_to_target_repository(self, compare_result: CompareResult) -> None:
        if compare_result.action == CompareResultAction.delete_from_target:
            self.write_deletion_to_target_repository(
                compare_result.dir_num,
                compare_result.track_num,
            )
        elif compare_result.action == CompareResultAction.copy_to_target:
            self.write_copy_to_target_repository(
                compare_result.dir_num,
                compare_result.track_num,
            )

    # ToDo: Rewrite to use CompareElement
    def write_deletion_to_target_repository(
        self,
        dir_number: int,
        track_number: int,
    ) -> None:
        # find element in target_repo that matches dir_number and track_number
        element_to_delete = next(
            (
                element
                for element in self._target_repo.elements
                if element.dir_number == dir_number
                and element.track_number == track_number
            ),
            None,
        )
        if element_to_delete is None:
            raise ValueError("Element to delete not found in the target repository")

        file_to_delete = os.path.join(
            self._target_repo_root_dir,
            str(dir_number).zfill(2),
            f"{str(track_number).zfill(3)}.{str(element_to_delete.file_type)}",
        )

        if os.path.isfile(file_to_delete):
            os.remove(file_to_delete)

    def write_copy_to_target_repository(
        self,
        dir_number: int,
        track_number: int,
    ) -> None:
        # find the element in the source repository that needs to be copied
        element_to_copy = next(
            (
                element
                for element in self._source_repo.elements
                if element.dir_number == dir_number
                and element.track_number == track_number
            ),
            None,
        )

        if element_to_copy is None:
            raise ValueError("Element to copy not found in the source repository")

        source_file_path = os.path.join(
            self._source_repo_root_dir,
            element_to_copy.dir,
            element_to_copy.file_name,
        )

        if not os.path.isfile(source_file_path):
            raise FileNotFoundError("Source file not found")

        target_file_path = os.path.join(
            self._target_repo_root_dir,
            str(dir_number).zfill(2),
            f"{str(track_number).zfill(3)}.{element_to_copy.file_type}",
        )

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        tags = (
            TagCollection(
                title=element_to_copy.title,
                artist=element_to_copy.artist,
                album=element_to_copy.album,
                track_number=element_to_copy.track_number,
            )
            if self._config.repository_processing.diff_method
            in {DiffMode.hash_and_tags, DiffMode.tags}
            else None
        )
        self._audio_manager.copy_audio(
            source_file_path,
            target_file_path,
            tags,
        )

    def _get_applied_config(self, element: RepositoryElement) -> RepositoryConfig:
        if element.repo_root_dir == self._target_repo_root_dir:
            applied_config = self._config.repository_target
        elif element.repo_root_dir == self._source_repo_root_dir:
            if element.dir in self._config_overrides:
                applied_config = self._config_overrides.get(
                    element.dir,
                    self._config.repository_source,
                )
            else:
                applied_config = self._config.repository_source
        else:
            raise ValueError("The element does not belong to any of the repositories")
        return applied_config

    def _reset(self) -> None:
        self._source_repo = Repository()
        self._target_repo = Repository()
        self._config_overrides = {}
