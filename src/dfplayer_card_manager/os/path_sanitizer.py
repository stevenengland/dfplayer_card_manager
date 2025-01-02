import os
import re


def sanitize_windows_volume_path(path: str) -> str:
    if re.match("^[a-zA-Z]:$", path):
        return path + os.sep
    return path.rstrip(os.sep) + os.sep
