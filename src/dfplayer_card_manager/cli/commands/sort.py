from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import print_ok


def sort(cli_context: CliContext, sd_card_path: str) -> None:
    if cli_context.fat_sorter.is_fat_volume_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted, nothing to do.")
        exit(0)
    cli_context.fat_sorter.sort_fat_volume(sd_card_path)
    print_ok(f"{sd_card_path} has been sorted.")
