from pydantic import BaseModel, Field

from dfplayer_card_manager.repository.detection_source import DetectionSource
from dfplayer_card_manager.repository.diff_modes import DiffMode


class RepositoryConfig(  # type: ignore[misc]
    BaseModel,
):  # Default configuration for source files and its contents
    valid_subdir_pattern: str | None = Field(
        default=None,  # Default regex pattern to match any directory
    )
    valid_subdir_files_pattern: str | None = Field(
        default=None,  # Default regex pattern to match any file
    )

    album_source: DetectionSource | None = Field(default=None)
    album_match: int | None = Field(default=None)

    artist_source: DetectionSource | None = Field(default=None)
    artist_match: int | None = Field(default=None)

    dir_number_source: DetectionSource | None = Field(default=None)
    dir_number_match: int | None = Field(default=None)

    title_source: DetectionSource | None = Field(default=None)
    title_match: int | None = Field(default=None)

    track_number_source: DetectionSource | None = Field(default=None)
    track_number_match: int | None = Field(default=None)


class ProcessingConfig(BaseModel):  # type: ignore[misc]
    diff_method: DiffMode | None = Field(default=None)
    overrides_file_name: str | None = Field(default=None)


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


class OverrideConfig(BaseModel):  # type: ignore[misc]
    repository_source: RepositoryConfig = Field(
        default_factory=RepositoryConfig,
    )
    repository_processing: ProcessingConfig = Field(
        default_factory=ProcessingConfig,
    )
