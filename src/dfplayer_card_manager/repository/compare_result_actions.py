from enum import Enum


class CompareResultAction(Enum):
    delete_from_target = "delete_from_target"
    copy_to_target = "copy_to_target"
    no_change = "no_change"
