import eyed3

from src.mp3.tag_collection import TagCollection
from src.mp3.tag_error import TagError
from src.mp3.tag_manager_interface import TagManagerInterface


class Eyed3TagManager(TagManagerInterface):

    def read_id3_tags(self, file_path: str) -> TagCollection:
        audio = eyed3.load(file_path)
        tag_collection = TagCollection()
        # Check if ID3v2 tag exists and is version 2.4
        if audio.tag and audio.tag.version[0] == 4:
            tags = audio.tag.v2
            tag_collection.title = tags.title
            tag_collection.artist = tags.artist
            tag_collection.album = tags.album
            tag_collection.track_number = tags.track_num[0]
        else:
            raise TagError("Invalid or unsupported audio tag.")
        return tag_collection
