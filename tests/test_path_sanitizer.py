import os

import pytest

from dfplayer_card_manager.os import path_sanitizer


class TestPathSanitation:
    @pytest.mark.parametrize(
        "path",
        [
            "E:",
            "E:\\",
        ],
    )
    def test_sanitize_windows_volume_path(self, path):
        # GIVEN
        path = "E:\\"
        # WHEN
        sanitized_path = path_sanitizer.sanitize_windows_volume_path(path)
        # THEN
        assert sanitized_path == f"E:{os.sep}"
