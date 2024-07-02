import re
import statistics
from datetime import timedelta
from typing import Iterator

from chatminer.model.block import Block
from chatminer.model.message import Message

BLOCK_MAX_INTERVAL = timedelta(hours=1)


def build_blocks(messages: list[Message]) -> Iterator[Block]:
    current_block = Block(messages[0])
    prev_time = messages[0].time
    for message in messages[1:]:
        if message.sender == current_block.sender and message.time - prev_time < BLOCK_MAX_INTERVAL:
            current_block.add(message)
        else:
            yield current_block
            current_block = Block(message)
        prev_time = message.time


def average_length(messages: list[Message]) -> float:
    lengths = [len(message.text) for message in messages]
    return round(statistics.fmean(lengths), 2)


def average_words(messages: list[Message]) -> float:
    wordcounts = [len(re.split(r"\s+", message.text)) for message in messages]
    return round(statistics.fmean(wordcounts), 2)


def average_block_size(blocks: list[Block]) -> float:
    sizes = [len(block) for block in blocks]
    return round(statistics.fmean(sizes), 2)
