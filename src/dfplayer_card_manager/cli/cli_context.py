from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from dfplayer_card_manager.config.configuration import Configuration
from dfplayer_card_manager.dfplayer.dfplayer_card_content_checker import (
    DfPlayerCardContentChecker,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_interface import (
    DfPlayerCardManagerInterface,
)
from dfplayer_card_manager.fat.fat_sorter_interface import FatSorterInterface
from dfplayer_card_manager.logging.logger_interface import LoggerInterface


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class CliContext:
    card_manager: DfPlayerCardManagerInterface | None = Field(default=None)
    configuration: Configuration | None = Field(default=None)
    content_checker: DfPlayerCardContentChecker | None = Field(default=None)
    fat_sorter: FatSorterInterface | None = Field(default=None)
    logger: LoggerInterface | None = Field(default=None)
