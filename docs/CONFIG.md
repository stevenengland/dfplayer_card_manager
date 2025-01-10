# Configuration

## Default file and folder structures enforced by this program

By default this program enforces how the files and folders on the SD card will be structured and has some expectations on how files and folders should look like in your source audio repository. The latter is by default what I personally use a lot but this can be changed easily.

### SD card

On the SD card the program will accept root level folders from 00 to 99. Within the subdirectories files are valid if they are between 001.mp3 and 255.mp3

```
sd_card_root
└── 01/
|    ├── 001.mp3
|    ├── 002.mp3
|    ├── ...
|    └── 255.mp3
|
└── ../
└── 99/
```

### Audio file repository

By default the files and folders are expected to be in this format (capital words are placeholders and can be written in lower case, upper case and can contain special characters). The dots are the seperating the information. See below how you can change this behaviour.

```
audio_repo_root
└── 01.ARTIST.ALBUM/
|   ├── 001.TITLE.mp3
|   ├── 002.TITLE.mp3
|   ├── ...
|   └── 255.TITLE.mp3
├── ...
└── 99.ARTIST.ALBUM/
```

## Configurations for the file and folder structure of the source audio repository

In the directory where you store the original audio files that can be synced to the SD card, you can place a configuration file named `dfplayer_card_manager.yaml` where you can override the default behavior of the `sync` command. You can also place further same named files in subdirectories of your repository to override the settings for just one directory during the sync process.

The `dfplayer_card_manager.yaml` file can contain options for two blocks: Options regarding the source audio repository itself (`repository_source`) and special options regarding the sync behaviour (`repository_processing`)

Here is an example:

```
audio_repo_root
└── 01.superstars.bestoff/
|   ├── 001.supertitleone.mp3
|   ├── 002.anotherone.mp3
|   ├── ...
|   ├── 255
|   └── dfplayer_card_manager.yaml (override per directory)
├── ...
├── 99.more.stuff/
└── dfplayer_card_manager.yaml (main config)
```

---

## 1. `repository_source`

| Property                     | Type                        | Description                                                                                                                                                                 |
| ---------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `valid_subdir_pattern`       | string &#124; None          | Regex to match directories in the repository path that shall be synced                                                                                                      |
| `valid_subdir_files_pattern` | string &#124; None          | Regex to match valid file names within the sub directories identified via `valid_subdir_pattern`                                                                            |
| `album_source`               | DetectionSource &#124; None | Source to detect the album information                                                                                                                                      |
| `album_match`                | integer &#124; None         | Additional matching numeric value for album detection                                                                                                                       |
| `artist_source`              | DetectionSource &#124; None | Source to detect the artist information                                                                                                                                     |
| `artist_match`               | integer &#124; None         | Additional matching numeric value for artist detection                                                                                                                      |
| `dir_number_source`          | DetectionSource &#124; None | Source for detecting the directory number. Must evaluate to a textual representation of a number between 00 and 99. Textual means, that leading zeros are allowed. Like 01. |
| `dir_number_match`           | integer &#124; None         | Additional matching numeric value for directory number detection                                                                                                            |
| `title_source`               | DetectionSource &#124; None | Source to detect the track title information                                                                                                                                |
| `title_match`                | integer &#124; None         | Additional matching numeric value for track title detection                                                                                                                 |
| `track_number_source`        | DetectionSource &#124; None | Source to detect the track number. Must evaluate to a textual representation of a number between 1 and 255. Textual means, that leading zeros are allowed. Like 001.        |
| `track_number_match`         | integer &#124; None         | Additional matching numeric value for track number detection                                                                                                                |

---

## 2. `repository_processing`

| Property    | Type                 | Description                                                                          |
| ----------- | -------------------- | ------------------------------------------------------------------------------------ |
| diff_method | DiffMode &#124; None | Approach for detecting differences between files on the SD card and thsos repository |

## `DiffMode`

If there are two files given:

- sd_root/01/001.mp3
- audio_repo_root/01.superstars.bestoff/001.supertitleone.mp3
  then the `sync` command can be instructed how to tell if the file on the SD card needs to be overwritten.

> Hint: The `sync` command will determine attributes like title and artist from the file in the audio repository (identified by `DetectionSorces`) and will add them as ID3 tags to the file stored on the SD card.

| Value         | Description                                                                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| none          | Does not compare file contents, only checks file existence (in the above scenario nothing will be done)                                                                   |
| hash          | Compares audio contents (tags excluded, only the audio portion is considered) by calculating and comparing the file content hashes                                        |
| tags          | Compares metadata (ID3 tags) of the file on the SD card for differences compared to the attributes of the file in the audio repository identified via `DetectionSources`. |
| hash_and_tags | Uses both hash and tag comparison.                                                                                                                                        |

## `DetectionSource`

| Value      | Description                                                           |
| ---------- | --------------------------------------------------------------------- |
| `dirname`  | Extracts metadata from the parent directory name of the audio file.   |
| `filename` | Extracts metadata from the filename of the audio file.                |
| `tag`      | Extracts metadata from any applicable tags (ID3 tags in an MP3 file). |

If the detection source is set to `dirname` or `filename` the corresponding match attribute needs to be filled and the subdir or subdir filename pattern needs to include a match group.

Example:

```
# file name for the example case = 001.supertitleone.mp3
# yaml content:
repository_source:
  valid_subdir_files_pattern: '^(\d{3})\.(.*?)\.mp3$'
  title_source: "filename"
  title_match: 2
```

Here the title would be the content of the second capturing group which would evaluate to 'supertitleone'
