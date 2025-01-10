# DfPlayer (Mini) Card Manager

This package is intended to manage SD cards that are used in DFROBOTs DFPlayer SD card reader.

You may ask: Why not just copying my audio files to the SD card and instead use this package to do the job? Answer: The cards filesystem and file structure need to follow certain rules. Therefore this package offers

- several checks and cleanup methods to be conform with the rules
- configurable music repository to SD card syncing mechanisms

# Features

- Perform file system checks (FAT type, allocation unit size, FAT sorting state)
- Delete undesireable files and folders from the SD card
- Apply FAT sorting to the SD card
- Sync audio files from a music repository (on any disk or filesystem) to the SD card

## What is (currently) not covered?

- SD card formatting
- Audio types: WAV (-> only MP3 is supported)

# Usage guide

The program can be run on Windows, Linux and Mac computers. All that is needed to use the DfPlayer Card Manager, is to have Python installed on your system. Then it is as easy as installing this package via pip:

```sh
pip install dfplayer-card-manager
```

## General Usage Instruction

To run the DfPlayer Card Manager, use the following command structure:

```sh
Usage: dfplayer-card-manager [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose             -v      INTEGER  [default: 0]                                                                                                                                 │
│ --install-completion                   Install completion for the current shell.                                                                                                    │
│ --show-completion                      Show completion for the current shell, to copy it or customize the installation.                                                             │
│ --help                                 Show this message and exit.                                                                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ check                                                                                                                                                                               │
│ sort                                                                                                                                                                                │
│ clean                                                                                                                                                                               │
│ sync                                                                                                                                                                                │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Available Commands

- [`check`](#check)
- [`sort`](#sort)
- [`clean`](#clean)
- [`sync`](#sync)

## Detailed Usage Instructions

### `check`

The `check` command is intended to check the SD card for common errors and validate its structure. These checks are performed:

- Filesystem: Is the SD card FAT32 formatted?
- Filesystem: Is the allocation unit size correct (32 kbits expected)
- Filesystem: Is the FAT volume sorted?
- Structure: Do the root directory or the subdirectories contain any undesireable files and folders?
- Structure: Do the root directory or the subdirectory have any gaps in the numbered items available?

**Usage:**

```sh
dfplayer-card-manager check <sd_card_path>
```

**Example:**

```sh
dfplayer-card-manager check /media/SDCARD
```

**Description:**

- `<sd_card_path>`: The path to the SD card. For example, `/media/SDCARD` or `E:\`.

### `sort`

The `sort` command is intended to apply FAT sorting to the SD card to ensure files and folders are in the correct order.

**Usage:**

```sh
dfplayer-card-manager sort <sd_card_path>
```

**Example:**

```sh
dfplayer-card-manager sort /media/SDCARD
```

**Description:**

- `<sd_card_path>`: The path to the SD card. For example, `/media/SDCARD` or `D:\`.

### `clean`

The `clean` command is intended to remove unwanted entries from the SD card. It can be run in a dry run mode to preview changes.

**Usage:**

```sh
dfplayer-card-manager clean <sd_card_path> [--dry-run]
```

**Example:**

```sh
dfplayer-card-manager clean /media/SDCARD --dry-run
```

**Description:**

- `<sd_card_path>`: The path to the SD card. For example, `/media/SDCARD` or `D:\`.
- `--dry-run`: Optional flag to preview the changes without actually removing any files.

### `sync`

The `sync` command is intended to synchronize the content from a repository folder to SD card. It can be run in a dry run mode to preview changes. See [CONFIG.md](./docs/CONFIG.md) for more information on which folder and file structure for the music repository is expected by default and how you can change these settings.

**Usage:**

```sh
dfplayer-card-manager sync <sd_card_path> <repository_path> [--dry-run]
```

**Example:**

```sh
dfplayer-card-manager sync /media/SDCARD /home/user/music --dry-run
```

**Description:**

- `<sd_card_path>`: The path to the SD card. For example, `/media/SDCARD` or `D:\`.
- `<repository_path>`: The path to the repository. For example, `/home/user/music` or `C:\Users\me\Music`.
- `--dry-run`: Optional flag to preview the changes without actually synchronizing any files.

# Projects that use DfPlayer Mini

- [TonUINO](https://www.tonuino.de/TNG/) -> A do it yourself musicbox (not only) for children (as a free alternative for [Tonie boxes](https://tonies.com/de-de/tonieboxen/)).
