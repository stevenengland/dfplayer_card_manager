import os
import sys
from pathlib import Path


# Read the path of the sdcard mount from the args.
# Create a bunch of files and directories (if either of them does not exist yet) on the sdcard.
def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: prepare_sd_card_for_check_tests.py <sdcard_path>")
        return
    sdcard_path = Path(sys.argv[1])
    if not sdcard_path.exists():
        print(f"Path {sdcard_path} does not exist.")
        exit(1)
    dirs_to_create = [
        "mp3",
        "advert",
        "01",
        "02",
        "03",
        "05",
        "04",
        "07",
        ".git",
        os.path.join("01", "001"),
        os.path.join("05", "002"),
    ]
    files_to_create = [
        "readme.txt",
        "unwanted.mp3",
        os.path.join("01", "001", "001.mp3"),
        os.path.join("01", "001.mp3"),
        os.path.join("01", "003.mp3"),
        os.path.join("01", "002.mp3"),
        os.path.join("02", "001.mp3"),
        os.path.join("02", "003.mp3"),
    ]
    for directory_to_create in dirs_to_create:
        (sdcard_path / directory_to_create).mkdir(exist_ok=True)
    for name in files_to_create:
        file_path = sdcard_path / name
        if not file_path.exists():
            file_path.touch()
    print("SD card preparation done.")


if __name__ == "__main__":
    main()
