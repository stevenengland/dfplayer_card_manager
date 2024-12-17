from dataclasses import dataclass, field


@dataclass
class RepositoryTargetConfig:  # Default configuration for the SD card and its contents
    root_dir: str = ""  # Default root directory
    valid_subdir_pattern: str = (
        r"^\d{2}$"  # Default regex pattern to match any directory
    )
    valid_subdir_files_pattern: str = (
        r"\d{3}\.mp3"  # Default regex pattern to match any file
    )


@dataclass
class RepositorySourceConfig:  # Default configuration for the SD card and its contents
    root_dir: str = ""  # Default root directory
    valid_subdir_pattern: str = (
        r"^\d{2}\..*$"  # Default regex pattern to match any directory
    )
    valid_subdir_files_pattern: str = (
        r"^\d{3}\..*\.mp3$"  # Default regex pattern to match any file
    )


@dataclass
class SubdirsConfig:
    valid_file_pattern: str = "^.*$"  # Default regex pattern to match any file


@dataclass
class TagsConfig:
    track_number_source: str = "filename"  # Default track source
    track_number_pattern: str = (
        r"\d{3}.*\.mp3"  # Default regex pattern for track filenames
    )


@dataclass
class Configuration:
    repository_target: RepositoryTargetConfig = field(
        default_factory=RepositoryTargetConfig,
    )
    repository_source: RepositorySourceConfig = field(
        default_factory=RepositorySourceConfig,
    )
    subdirs: SubdirsConfig = field(default_factory=SubdirsConfig)
    tags: TagsConfig = field(default_factory=TagsConfig)
