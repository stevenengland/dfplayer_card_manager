from src.config.configuration import Configuration, RepositorySourceConfig
from src.dfplayer_card_manager_interface import DfPlayerCardManagerInterface
from src.mp3.audio_file_manager_interface import AudioFileManagerInterface
from src.repository import config_override, repository_finder
from src.repository.repository_element import RepositoryElement


class DfPlayerCardManager(DfPlayerCardManagerInterface):
    def __init__(self, config: Configuration, audio_manager: AudioFileManagerInterface):
        self._config = config
        self._config_overrides: dict[str, RepositorySourceConfig] = {}
        self._audio_manager = audio_manager
        self._source_repo: list[RepositoryElement] = []
        self._target_repo: list[RepositoryElement] = []

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

    def init_repositories(self) -> None:
        source_repository_tree = self.get_source_repository_tree()
        target_repository_tree = self.get_target_repository_tree()
        for source_subdirectory, source_file in source_repository_tree:
            # create a repository element with subdir and file
            element = RepositoryElement()
            element.dir = source_subdirectory
            element.file_name = source_file
            self._source_repo.append(element)
        for target_subdirectory, target_file in target_repository_tree:
            # create a repository element with subdir and file
            element = RepositoryElement()
            element.dir = target_subdirectory
            element.file_name = target_file
            self._target_repo.append(element)

    def read_config_overrides(self) -> None:
        if self._config.repository_source.root_dir is None:
            raise ValueError("Repository source root directory is not set")
        self._config_overrides = config_override.get_config_overrides(
            self._config.repository_source.root_dir,
            # get all distinct subdirs from the source repository
            [element.dir for element in self._source_repo],
            self._config.overrides_file_name,
        )

    def get_target_repository_tree(self) -> list[tuple[str, str]]:
        if self._config.repository_target.root_dir is None:
            raise ValueError("Repository target root directory is not set")
        return repository_finder.get_repository_tree(
            self._config.repository_target.root_dir,
            self._config.repository_target.valid_subdir_pattern,
            self._config.repository_target.valid_subdir_files_pattern,
        )

    def get_source_repository_tree(
        self,
    ) -> list[tuple[str, str]]:
        if self._config.repository_source.root_dir is None:
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
            self._config.repository_source.root_dir,
            self._config.repository_source.valid_subdir_pattern,
            self._config.repository_source.valid_subdir_files_pattern,
            valid_subdir_files_pattern_overrides,
        )
