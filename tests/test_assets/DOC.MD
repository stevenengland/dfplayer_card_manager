# Asset description

- 1 - Metadata block without actual Metadata -> 3605 bytes of content and 45 bytes of metadata
- 2 - Tags set to certain values -> 3605 bytes of metadata and
- 3 - No metatdata available (via eyed3 --remove-all 0003.mp3) -> 3605 bytes of pure content

## Use Cases

- ctt - copy to target
- dft - delete from target
- tne - target does not exist
- swt - source with tags
- smt - source missing tags
- tdt - target with different tag
- tmt - target missing tags
