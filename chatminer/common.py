import inspect
from milc import cli


def log(text: str) -> None:
    cli.log.info(f'[chatminer] - {text}')


def log_multiline(text: str) -> None:
    for line in text.splitlines():
        cli.log.info(f'[chatminer] - {line}')


def error(text: str) -> None:
    _, filename, _, func, _, _ = inspect.stack()[1]
    cli.log.error(f"[chatminer][{filename.split('/')[-1]}][{func}()] - ERROR: {text}")
