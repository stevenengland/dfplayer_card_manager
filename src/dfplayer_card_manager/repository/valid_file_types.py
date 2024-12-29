from enum import Enum


class ValidFileType(  # noqa: WPS600, ToDo: Fix by using StrEnum when using python 11
    str,
    Enum,
):
    mp3 = "mp3"

    def __str__(self) -> str:
        return self.value
