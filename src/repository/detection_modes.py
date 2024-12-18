from dataclasses import dataclass

from src.repository.detection_source import DetectionSource


@dataclass
class DetectionMode:
    def __init__(self) -> None:
        self.info_source = DetectionSource.tag
        self.info_pattern = ""
        self.info_pattern_match = 0
