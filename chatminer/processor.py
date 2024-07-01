import re
import statistics
from collections import defaultdict
from typing import Callable

from chatminer.model.message import Message


def group_messages(messages: list[Message], func: Callable[[Message], str]) -> dict[str, list[Message]]:
    output = defaultdict(list)
    for message in messages:
        output[func(message)].append(message)
    return dict(output)


def average_length(messages: list[Message]) -> float:
    lengths = [len(message.text) for message in messages]
    return round(statistics.fmean(lengths), 2)


def average_words(messages: list[Message]) -> float:
    wordcounts = [len(re.split(r"\s+", message.text)) for message in messages]
    return round(statistics.fmean(wordcounts), 2)
