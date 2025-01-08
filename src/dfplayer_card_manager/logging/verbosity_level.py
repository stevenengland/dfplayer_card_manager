from enum import IntEnum


class VerbosityLevel(IntEnum):
    trace = 4
    debug = 3
    info = 2  # noqa: WPS110
    warn = 1
    error = 0
