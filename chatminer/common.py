import inspect
from collections import defaultdict
from typing import Iterable, Any, Callable

from milc import cli

from chatminer.model.message import Message


def log(text: str) -> None:
    cli.log.info(f"[chatminer] - {text}")


def log_multiline(text: str) -> None:
    for line in text.splitlines():
        cli.log.info(f"[chatminer] - {line}")


def warn(text: str) -> None:
    cli.log.warn(f"[chatminer] - WARNING: {text}")


def error(text: str) -> None:
    _, filename, _, func, _, _ = inspect.stack()[1]
    cli.log.error(f"[chatminer][{filename.split('/')[-1]}][{func}()] - ERROR: {text}")


def group_by(func: Callable[[Message], str], items: Iterable[Any]) -> dict[str, list[Any]]:
    output = defaultdict(list)
    for item in items:
        output[func(item)].append(item)
    return dict(output)


def truncate(string: str, max_length: int) -> str:
    return string[:max_length] + '...' if len(string) > max_length else string
