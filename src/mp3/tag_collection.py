from dataclasses import dataclass


@dataclass
class TagCollection:
    def __init__(self) -> None:
        self.title = ""
        self.artist = ""
        self.album = ""
        self.track_number = 0
