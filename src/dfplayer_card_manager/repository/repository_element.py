from pydantic import Field
from pydantic.dataclasses import dataclass

from dfplayer_card_manager.repository.valid_file_types import ValidFileType


@dataclass
class RepositoryElement:  # noqa: WPS230
    tree_id: str | None = Field(default=None)
    repo_root_dir: str = Field(default="")
    dir: str = Field(default="")
    file_name: str = Field(default="")
    title: str | None = Field(default=None)
    artist: str | None = Field(default=None)
    album: str | None = Field(default=None)
    track_number: int | None = Field(default=None)
    dir_number: int | None = Field(default=None)
    hash: str | None = Field(default=None)
    file_type: ValidFileType | None = Field(default=None)
