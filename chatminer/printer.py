from tabulate import tabulate
from emoji import replace_emoji
from typing import Any

from chatminer.common import log_multiline


def print_table(values: list) -> None:
    values_sanitized = [[sanitize_if_text(value) for value in row] for row in values]
    table = tabulate(values_sanitized, headers="firstrow", tablefmt="github")
    log_multiline(table)


def sanitize_if_text(value: Any) -> Any:
    if type(value) == str:
        return replace_emoji(value, '')
    return value
