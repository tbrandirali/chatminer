import re

from chatminer.model.message import Message
from chatminer.model.notification import Notification

line_regex = r'^[0-9]+/[0-9]+/[0-9]+.*'


def parse(lines: list[str]) -> (list[Message], list[Notification]):
    lines = remove_newlines(lines)
    lines = [line.replace(" ", " ") for line in lines]
    message_strings, notifications_strings = filter_notifications(lines)
    messages = [Message.from_string(i + 1, mstring) for i, mstring in enumerate(message_strings)]
    notifications = [Notification.from_string(i + 1, nstring) for i, nstring in enumerate(notifications_strings)]
    return messages, notifications


def remove_newlines(lines: list[str]) -> list[str]:
    output = []
    for i, line in enumerate(lines):
        if not line or not re.search(line_regex, line):
            output[-1] += line
        else:
            output.append(line)
    return output


def filter_notifications(lines: list[str]) -> (list[str], list[str]):
    messages = []
    notifications = []
    for line in lines:
        text = line.split(" - ", maxsplit=1)[1]
        if re.match(r".*: .*", text):
            messages.append(line)
        else:
            notifications.append(line)
    return messages, notifications
