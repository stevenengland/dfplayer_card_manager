from enum import Enum


class DiffMode(Enum):
    none = 0
    hash = 1
    tags = 2
    hash_and_tags = 3
