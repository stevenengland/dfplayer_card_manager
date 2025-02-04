import errno
import os


def probe_is_busy(device_path: str) -> bool:
    fd: int | None = None
    try:
        fd = os.open(device_path, os.O_RDWR | os.O_NONBLOCK)
    except OSError as os_error:
        if os_error.errno == errno.EBUSY:
            return True
    finally:
        if fd:
            os.close(fd)
    return False
