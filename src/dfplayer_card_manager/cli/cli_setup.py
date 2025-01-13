from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.config import config_checker
from dfplayer_card_manager.config.configuration import (
    Configuration,
    ProcessingConfig,
    RepositoryConfig,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_content_checker import (
    DfPlayerCardContentChecker,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager import (
    DfPlayerCardManager,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_interface import (
    DfPlayerCardManagerInterface,
)
from dfplayer_card_manager.fat.fat_sorter import FatSorter
from dfplayer_card_manager.fat.fat_sorter_interface import FatSorterInterface
from dfplayer_card_manager.logging.logger import Logger
from dfplayer_card_manager.mp3.audio_file_manager import AudioFileManager
from dfplayer_card_manager.repository.detection_source import DetectionSource
from dfplayer_card_manager.repository.diff_modes import DiffMode


def setup_cli_context() -> CliContext:
    cli_context = CliContext()
    cli_context.logger = Logger()
    cli_context.configuration = (
        _setup_default_config()
    )  # only partially overriden in sync command
    config_checker.check_config(cli_context.configuration)
    cli_context.fat_sorter = _setup_fat_sorter()
    cli_context.content_checker = _setup_content_checker(
        config=cli_context.configuration.repository_target,
    )
    cli_context.card_manager = _setup_card_manager(
        config=cli_context.configuration,
        logger=cli_context.logger,
    )
    return cli_context


def _setup_default_config() -> Configuration:
    tmp_config = Configuration()
    tmp_config.repository_target = RepositoryConfig(
        valid_subdir_pattern=r"^(\d{2})$",
        valid_subdir_files_pattern=r"^(\d{3})\.mp3$",
        album_source=DetectionSource.tag,
        artist_source=DetectionSource.tag,
        dir_number_source=DetectionSource.dirname,
        dir_number_match=1,
        title_source=DetectionSource.tag,
        track_number_source=DetectionSource.filename,
        track_number_match=1,
    )
    tmp_config.repository_source = RepositoryConfig(
        valid_subdir_pattern=r"^(\d{2})\.(.*?)\.(.*?)$",
        valid_subdir_files_pattern=r"^(\d{3})\.(.*?)\.mp3$",
        album_source=DetectionSource.dirname,
        album_match=3,
        artist_source=DetectionSource.dirname,
        artist_match=2,
        dir_number_source=DetectionSource.dirname,
        dir_number_match=1,
        title_source=DetectionSource.filename,
        title_match=2,
        track_number_source=DetectionSource.filename,
        track_number_match=1,
    )
    tmp_config.repository_processing = ProcessingConfig(
        diff_method=DiffMode.hash_and_tags,
        overrides_file_name="dfplayer_card_manager.yaml",
    )
    return tmp_config


def _setup_fat_sorter() -> FatSorterInterface:
    return FatSorter()


def _setup_content_checker(config: RepositoryConfig) -> DfPlayerCardContentChecker:
    if (
        not config.valid_subdir_files_pattern
        or not config.track_number_match
        or not config.valid_subdir_pattern
    ):
        raise DfPlayerCardManagerError("Missing config values for content checker.")
    return DfPlayerCardContentChecker(
        valid_root_dir_pattern=config.valid_subdir_pattern,
        valid_subdir_files_pattern=config.valid_subdir_files_pattern,
        valid_subdir_files_track_number_match=config.track_number_match,
        root_dir_exceptions={"mp3", "advert"},
    )


def _setup_card_manager(
    config: Configuration,
    logger: Logger,
) -> DfPlayerCardManagerInterface:

    return DfPlayerCardManager(
        source_repo_root_dir="",
        target_repo_root_dir="",
        audio_manager=AudioFileManager(),
        config=config,
        logger=logger,
    )
