from pydantic import Field
from pydantic.dataclasses import dataclass

from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


@dataclass
class CompareResult:
    dir_num: int | None = Field(default=None)
    track_num: int | None = Field(default=None)
    source_element: RepositoryElement | None = Field(default=None)
    target_element: RepositoryElement | None = Field(default=None)
    action: CompareResultAction | None = Field(default=None)
