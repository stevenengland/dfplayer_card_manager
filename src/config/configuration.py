from pydantic import BaseModel, Field

from src.repository.detection_source import DetectionSource
from src.repository.diff_modes import DiffMode


class RepositoryConfig(  # type: ignore[misc]
    BaseModel,
):  # Default configuration for source files and its contents
    # ToDo: Remove the following Field
    root_dir: str | None = Field(
        default=None,
    )  # Default root directory, set by command line argument but not by configuration reader
    valid_subdir_pattern: str | None = Field(
        default=None,  # Default regex pattern to match any directory
    )
    valid_subdir_files_pattern: str | None = Field(
        default=None,  # Default regex pattern to match any file
    )
    # ToDo: Remove the following Field
    diff_method: DiffMode | None = Field(default=None)

    album_source: DetectionSource | None = Field(default=None)
    album_match: int | None = Field(default=None)

    artist_source: DetectionSource | None = Field(default=None)
    artist_match: int | None = Field(default=None)

    title_source: DetectionSource | None = Field(default=None)
    title_match: int | None = Field(default=None)

    track_number_source: DetectionSource | None = Field(default=None)
    track_number_match: int | None = Field(default=None)


class ProcessingConfig(BaseModel):  # type: ignore[misc]
    diff_method: DiffMode | None = Field(default=None)
    overrides_file_name: str = Field(
        default=".dfplayer_card_manager.yaml",
    )


class Configuration(BaseModel):  # type: ignore[misc]
    repository_target: RepositoryConfig = Field(
        default_factory=RepositoryConfig,
        init=False,
    )
    repository_source: RepositoryConfig = Field(
        default_factory=RepositoryConfig,
        init=False,
    )
    repository_processing: ProcessingConfig = Field(
        default_factory=ProcessingConfig,
        init=False,
    )
    # ToDo: Remove the following Field
    overrides_file_name: str = Field(
        default=".dfplayer_card_manager.yaml",
        init=False,
    )


class OverrideConfig(BaseModel):  # type: ignore[misc]
    repository_source: RepositoryConfig = Field(
        default_factory=RepositoryConfig,
    )
    repository_processing: ProcessingConfig = Field(
        default_factory=ProcessingConfig,
    )
