from dataclasses import dataclass


@dataclass
class RepositoryElement:  # noqa: WPS230
    def __init__(self) -> None:
        self.tree_id = ""
        self.dir = ""
        self.file_name = ""
        self.title = ""
        self.artist = ""
        self.album = ""
        self.track_number = 0
