import re
import statistics
from collections import defaultdict
from datetime import timedelta
from typing import Callable

from chatminer.model.block import Block
from chatminer.model.message import Message

BLOCK_MAX_INTERVAL = timedelta(hours=1)


def group_messages(messages: list[Message], func: Callable[[Message], str]) -> dict[str, list[Message]]:
    output = defaultdict(list)
    for message in messages:
        output[func(message)].append(message)
    return dict(output)


def group_blocks(messages: list[Message]) -> list[Block]:
    current_block = Block(messages[0])
    blocks = [current_block]
    prev_time = messages[0].time
    for message in messages[1:]:
        if message.sender == current_block.sender and message.time - prev_time < BLOCK_MAX_INTERVAL:
            current_block.messages.append(message)
        else:
            current_block = Block(message)
            blocks.append(current_block)
        prev_time = message.time
    return blocks


def average_length(messages: list[Message]) -> float:
    lengths = [len(message.text) for message in messages]
    return round(statistics.fmean(lengths), 2)


def average_words(messages: list[Message]) -> float:
    wordcounts = [len(re.split(r"\s+", message.text)) for message in messages]
    return round(statistics.fmean(wordcounts), 2)
