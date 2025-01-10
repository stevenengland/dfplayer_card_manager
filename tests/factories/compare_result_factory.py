from faker import Faker

from dfplayer_card_manager.repository.compare_result import CompareResult

faker = Faker()


def create_compare_result(dir_num: int, track_num: int) -> CompareResult:
    return CompareResult(
        dir_num=dir_num,
        track_num=track_num,
        source_element=None,
        target_element=None,
        action=None,
    )
