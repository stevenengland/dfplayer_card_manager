from dataclasses import dataclass

from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


@dataclass
class Repository:
    def __init__(self) -> None:
        self.root_dir: str = ""
        self.elements: list[RepositoryElement] = []