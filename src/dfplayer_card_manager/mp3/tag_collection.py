from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class TagCollection:
    title: str | None = Field(default=None)
    artist: str | None = Field(default=None)
    album: str | None = Field(default=None)
    track_number: int | None = Field(default=None)
