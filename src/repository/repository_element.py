from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class RepositoryElement:  # noqa: WPS230
    tree_id: str | None = Field(default=None)
    repo_root_dir: str | None = Field(default=None)
    dir: str = Field(default="")
    file_name: str = Field(default="")
    title: str | None = Field(default=None)
    artist: str | None = Field(default=None)
    album: str | None = Field(default=None)
    track_number: int | None = Field(default=None)
    hash: str | None = Field(default=None)
