import re

from chatminer.model.message import Message
from chatminer.model.notification import Notification

notification_strings = [
    "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.",
    "Your security code with changed. Tap to learn more.",
    "changed their phone number to a new number. Tap to message or add the new number.",
    "changed their phone number. You're currently chatting with their new number. Tap to add it to your contacts.",
    "changed this group's icon"
]
line_regex = '^[0-9]+/[0-9]+/[0-9]+.*'


def parse(lines: list[str]) -> (list[Message], list[Notification]):
    lines = remove_newlines(lines)
    message_strings, notifications_strings = filter_lines(lines)
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


def filter_lines(lines: list[str]) -> (list[str], list[str]):
    messages = []
    notifications = []
    for line in lines:
        if not any(ext in line for ext in notification_strings):
            messages.append(line)
        else:
            notifications.append(line)
    return messages, notifications
