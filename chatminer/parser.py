import re
from typing import Iterator, Iterable, TypeVar, Type

from chatminer import common
from chatminer.model.message import Message
from chatminer.model.notification import Notification

line_pattern = r"[0-9]+/[0-9]+/[0-9]+.*"

ChatElement = TypeVar("ChatElement", Message, Notification)


def parse(lines: Iterable[str]) -> (Iterator[Message], Iterator[Notification]):
    lines_trimmed = compact_by_pattern(lines, line_pattern)
    lines_cleaned = substitute(lines_trimmed, " ", " ")
    message_strings, notifications_strings = filter_notifications(lines_cleaned)
    messages = build_elements(message_strings, Message)
    notifications = build_elements(notifications_strings, Notification)
    return messages, notifications


def compact_by_pattern(lines: Iterable[str], pattern: str) -> Iterator[str]:
    prev_line = None
    for i, line in enumerate(lines):
        if not line or not re.match(pattern, line):
            if i == 0:
                raise ValueError("Expected the first line in the file to be a message")
            prev_line += line
        else:
            if i != 0:
                yield prev_line
            prev_line = line


def substitute(lines: Iterable[str], old: str, new: str) -> Iterator[str]:
    for line in lines:
        yield line.replace(old, new)


def filter_notifications(lines: Iterable[str]) -> (list[str], list[str]):
    messages = []
    notifications = []
    for line in lines:
        text = line.split(" - ", maxsplit=1)[1]
        if re.match(r".*: .*", text):
            messages.append(line)
        else:
            notifications.append(line)
    return messages, notifications


def build_elements(strings: Iterable[str], type: Type[ChatElement]) -> Iterator[ChatElement]:
    prev_element = None
    for i, string in enumerate(strings):
        element = type.from_string(i + 1, string)
        if prev_element and element.time < prev_element.time:
            common.warn(f"Chronological ordering broken: [{element}] after [{prev_element}]")
        prev_element = element
        yield element
