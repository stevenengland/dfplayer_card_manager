from dataclasses import dataclass, field

from src.config.yaml_config import YamlObject
from src.repository.detection_source import DetectionSource
from src.repository.diff_modes import DiffMode


@dataclass
class RepositoryTargetConfig(
    YamlObject,
):  # Default configuration for the SD card and its contents
    root_dir: str = field(
        default="",  # Default root directory, set by command line argument but not by configuration reader
    )
    valid_subdir_pattern: str = field(
        default=r"^\d{2}$",  # Default regex pattern to match any directory, not read by configuration reader
    )
    valid_subdir_files_pattern: str = field(
        default=r"\d{3}\.mp3",  # Default regex pattern to match any file, not read by configuration reader
    )


@dataclass
class RepositorySourceConfig(
    YamlObject,
):  # Default configuration for source files and its contents
    root_dir: str = field(
        default="",
    )  # Default root directory, set by command line argument but not by configuration reader
    valid_subdir_pattern: str = field(
        default=r"^\d{2}\..*$",  # Default regex pattern to match any directory
    )
    valid_subdir_files_pattern: str = field(
        default=r"^\d{3}\..*\.mp3$",  # Default regex pattern to match any file
    )
    diff_method: DiffMode = field(default=DiffMode.hash_and_tags)

    title_source: DetectionSource = field(default=DetectionSource.tag)
    title_match: int = field(default=0)


@dataclass
class Configuration(YamlObject):
    repository_target: RepositoryTargetConfig = field(
        default_factory=RepositoryTargetConfig,
    )
    repository_source: RepositorySourceConfig = field(
        default_factory=RepositorySourceConfig,
    )
    overrides_file_name: str = field(
        default=".dfplayer_card_manager.yaml",
    )