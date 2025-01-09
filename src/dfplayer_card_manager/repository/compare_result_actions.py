from enum import Enum


class CompareResultAction(  # noqa: WPS600, ToDo: Fix by using StrEnum when using python 11
    str,
    Enum,
):
    delete_from_target = "delete_from_target"
    copy_to_target = "copy_to_target"
    no_change = "no_change"
    unstuff = "unstuff"

    def __str__(self) -> str:
        return self.value
