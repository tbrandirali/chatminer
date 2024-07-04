import re
import statistics
from datetime import timedelta
from typing import Iterator, Iterable

from chatminer.model.block import Block
from chatminer.model.message import Message

BLOCK_MAX_INTERVAL = timedelta(hours=1)


def build_blocks(messages: Iterable[Message]) -> Iterator[Block]:
    iterator = iter(messages)
    first_message = next(iterator)
    current_block = Block(first_message)
    prev_time = first_message.time
    for message in iterator:
        if message.sender == current_block.sender and message.time - prev_time < BLOCK_MAX_INTERVAL:
            current_block.add(message)
        else:
            yield current_block
            current_block = Block(message)
        prev_time = message.time


def average_length(messages: Iterable[Message]) -> float:
    lengths = map(lambda message: len(message.text), messages)
    return round(statistics.fmean(lengths), 2)


def average_words(messages: Iterable[Message]) -> float:
    wordcounts = map(lambda message: len(re.split(r"\s+", message.text)), messages)
    return round(statistics.fmean(wordcounts), 2)


def average_block_size(blocks: Iterable[Block]) -> float:
    sizes = map(lambda block: len(block), blocks)
    return round(statistics.fmean(sizes), 2)
