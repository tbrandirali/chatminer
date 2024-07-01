import re
import milc

from chatminer import parser, plotter, db, printer
from chatminer.common import log, error
from chatminer.processor import group_messages, average_words, average_length


@milc.cli.entrypoint('This is chatminer! Specify a command to use...')
def entrypoint(cli: milc.MILC) -> None:
    log('No subcommand specified!')


@milc.cli.argument('-i', '--input', help="Input text file")
@milc.cli.argument('-c', '--chat', help="The name to give to the imported chat")
@milc.cli.subcommand('Import a whatsapp chat as txt file into an SQL table')
def create(cli: milc.MILC) -> None:
    file_path = cli.args.input if cli.args.input else missing_arg("Input file path is required")
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]

    messages, notifications = parser.parse(lines)

    with db.create_connection() as conn:
        db.create_messages_table(conn, chat_name)
        db.insert_messages(conn, chat_name, messages)
        db.create_notifications_table(conn, f'{chat_name}_notifications')
        db.insert_notifications(conn, f'{chat_name}_notifications', notifications)


@milc.cli.argument('-c', '--chat', help="The name of the chat to delete")
@milc.cli.subcommand('Delete the database table for an imported chat')
def delete(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with db.create_connection() as conn:
        db.delete_table(conn, chat_name)
        db.delete_table(conn, f"{chat_name}_notifications")


@milc.cli.argument('-c', '--chat', help="The chat name to plot frequency for")
@milc.cli.argument('-k', '--keyword', help="A keyword to plot the frequency of in the given chat")
@milc.cli.subcommand('Plot the message frequency over time for a specific chat')
def frequency(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with db.create_connection() as conn:
        messages = db.get_all_messages(conn, chat_name)

    keyword = cli.args.keyword
    if keyword is not None:
        messages = [message for message in messages if re.search(keyword, message.text, re.IGNORECASE)]
    plotter.plot_frequency(messages, keyword)


@milc.cli.argument('-c', '--chat', help="The chat name to plot frequency for")
@milc.cli.argument('-k', '--keyword', help="A keyword to plot the frequency of in the given chat")
@milc.cli.subcommand('Plot the message frequency over time for each sender in a specific chat')
def frequency_per_sender(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with db.create_connection() as conn:
        messages = db.get_all_messages(conn, chat_name)

    keyword = cli.args.keyword
    if keyword is not None:
        messages = [message for message in messages if re.search(keyword, message.text, re.IGNORECASE)]
    plotter.plot_frequency_per_sender(messages, keyword)


@milc.cli.argument('-c', '--chat', help="The chat name to show notifications for")
@milc.cli.subcommand('Print all the notifications for a chat')
def notifications(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with db.create_connection() as conn:
        notifications = db.get_all_notifications(conn, chat_name)

    log(f"Showing {len(notifications)} notifications")
    for notification in notifications:
        log(f"{notification.time} - {notification.text}")


@milc.cli.argument('-c', '--chat', help="The chat name to show a summary for")
@milc.cli.subcommand('Print a summary of statistics for a chat')
def senders(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with db.create_connection() as conn:
        messages = db.get_all_messages(conn, chat_name)
    sender_messages = group_messages(messages, lambda msg: msg.sender)
    averages = [
        [sender, len(messages), average_words(messages), average_length(messages)]
        for sender, messages in sender_messages.items()
    ]
    averages = [["Sender", "Messages", "Avg. Words", "Avg. Length"]] + averages
    printer.print_table(averages)


@milc.cli.subcommand("Removes all files and databases persisted by chatminer on the local system")
def uninstall(cli: milc.MILC) -> None:
    db.delete_database()


def missing_arg(arg_name: str) -> None:
    error(f"{arg_name} is required!")
    exit(1)


def main() -> None:
    milc.cli()
