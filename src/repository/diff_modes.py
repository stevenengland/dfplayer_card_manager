from enum import Enum


class DiffMode(Enum):
    none = "none"
    hash = "hash"
    tags = "tags"
    hash_and_tags = "hash_and_tags"
