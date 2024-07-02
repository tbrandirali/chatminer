import re
from typing import Iterable, Any

from chatminer import common, parser, db, plotter, printer, processor


def create(file_path: str, chat_name: str) -> None:
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]

    messages, notifications = parser.parse(lines)

    with db.create_connection() as conn:
        db.create_messages_table(conn, chat_name)
        db.insert_messages(conn, chat_name, messages)
        db.create_notifications_table(conn, f'{chat_name}_notifications')
        db.insert_notifications(conn, f'{chat_name}_notifications', notifications)


def delete(chat_name: str) -> None:
    with db.create_connection() as conn:
        db.delete_table(conn, chat_name)
        db.delete_table(conn, f"{chat_name}_notifications")


def frequency(chat_name: str, keyword: str) -> None:
    with db.create_connection() as conn:
        messages = db.get_all_messages(conn, chat_name)

    if keyword is not None:
        messages = [message for message in messages if re.search(keyword, message.text, re.IGNORECASE)]
    plotter.plot_frequency(messages, keyword)


def frequency_per_sender(chat_name: str, keyword: str) -> None:
    with db.create_connection() as conn:
        messages = db.get_all_messages(conn, chat_name)

    if keyword is not None:
        messages = [message for message in messages if re.search(keyword, message.text, re.IGNORECASE)]
    plotter.plot_frequency_per_sender(messages, keyword)


def notifications(chat_name: str) -> None:
    with db.create_connection() as conn:
        notifications = db.get_all_notifications(conn, chat_name)

    common.log(f"Showing {len(notifications)} notifications")
    for notification in notifications:
        common.log(f"{notification.time} - {notification.text}")


def senders(chat_name: str) -> None:
    with db.create_connection() as conn:
        messages = db.get_all_messages(conn, chat_name)

    blocks = processor.build_blocks(messages)
    sender_blocks = common.group_by(lambda block: block.sender, blocks)
    sender_messages = common.group_by(lambda msg: msg.sender, messages)
    zipped_dicts = zip_dicts(sender_messages, sender_blocks)
    averages = [
        [
            sender,
            len(messages),
            processor.average_words(messages),
            processor.average_length(messages),
            processor.average_block_size(blocks)
        ] for sender, messages, blocks in zipped_dicts
    ]
    averages = [["Sender", "Messages", "Avg. Words", "Avg. Length", "Avg. Block Size"]] + averages
    printer.print_table(averages)


def uninstall() -> None:
    db.delete_database()


def flatten(iterables: list[Iterable[Any]]) -> list[Any]:
    output = []
    for iterable in iterables:
        output += iterable
    return output


def zip_dicts(*dcts: dict[str, Any]) -> tuple[str, dict[Any], dict[Any]]:
    if not dcts:
        return
    for i in set(dcts[0]).intersection(*dcts[1:]):
        yield (i,) + tuple(d[i] for d in dcts)
