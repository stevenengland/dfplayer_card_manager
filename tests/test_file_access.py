import errno
import os

from dfplayer_card_manager.os.file_access import probe_is_busy


def test_resource_is_busy(when):
    # GIVEN
    when(os).open(...).thenRaise(OSError(errno.EBUSY, "Resource is busy"))
    device_path = "/dev/sdb1"
    # WHEN
    probe_result = probe_is_busy(device_path)
    # THEN
    assert probe_result
    assert probe_result
