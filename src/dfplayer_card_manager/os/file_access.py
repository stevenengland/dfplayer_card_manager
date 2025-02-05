import errno
import os


# Unix only
def probe_is_busy(device_path: str) -> bool:
    fd: int | None = None
    flags = os.O_RDWR
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK
    try:
        fd = os.open(device_path, flags)
    except OSError as os_error:
        if os_error.errno == errno.EBUSY:
            return True
    finally:
        if fd:
            os.close(fd)
    return False
