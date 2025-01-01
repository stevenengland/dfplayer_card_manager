from rich import print


def print_ok(message: str, is_bullet: bool = False) -> None:
    bullet = "• " if is_bullet else ""
    print(f"[green]{bullet}{message}[/green]")


def print_warning(message: str, is_bullet: bool = False) -> None:
    bullet = "• " if is_bullet else ""
    print(f"[yellow]{bullet}{message}[/yellow]")


def print_error(message: str, is_bullet: bool = False) -> None:
    bullet = "• " if is_bullet else ""
    print(f"[red]{bullet}{message}[/red]")
