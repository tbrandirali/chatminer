import re
import milc

from chatminer import parser, viz, config, sqlitedb
from chatminer.common import log, error

configs = config.configs


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

    with sqlitedb.create_connection() as conn:
        sqlitedb.create_messages_table(conn, chat_name)
        sqlitedb.insert_messages(conn, chat_name, messages)
        sqlitedb.create_notifications_table(conn, f'{chat_name}_notifications')
        sqlitedb.insert_notifications(conn, f'{chat_name}_notifications', notifications)


@milc.cli.argument('-c', '--chat', help="The name of the chat to delete")
@milc.cli.subcommand('Delete the database table for an imported chat')
def delete(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with sqlitedb.create_connection() as conn:
        sqlitedb.delete_table(conn, chat_name)
        sqlitedb.delete_table(conn, f"{chat_name}_notifications")


@milc.cli.argument('-c', '--chat', help="The database table to plot frequency for")
@milc.cli.argument('-k', '--keyword', help="A keyword to plot the frequency of in the given chat")
@milc.cli.subcommand('Plot the message frequency over time for a specific chat')
def frequency(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with sqlitedb.create_connection() as conn:
        messages = sqlitedb.get_all_messages(conn, chat_name)

    keyword = cli.args.keyword
    if keyword is not None:
        messages = [message for message in messages if re.search(keyword, message.text, re.IGNORECASE)]
    viz.plot_frequency(messages, keyword)


@milc.cli.argument('-c', '--chat', help="The database table to plot frequency for")
@milc.cli.argument('-k', '--keyword', help="A keyword to plot the frequency of in the given chat")
@milc.cli.subcommand('Plot the message frequency over time for each sender in a specific chat')
def frequency_per_sender(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")

    with sqlitedb.create_connection() as conn:
        messages = sqlitedb.get_all_messages(conn, chat_name)

    keyword = cli.args.keyword
    if keyword is not None:
        messages = [message for message in messages if re.search(keyword, message.text, re.IGNORECASE)]
    viz.plot_frequency_per_sender(messages, keyword)


@milc.cli.argument('-n', '--name', help="The name of the configuration item to set, in dot notation (ex: 'database.host')")
@milc.cli.argument('-v', '--value', help="The value to set the configuration item to")
@milc.cli.argument('-r', '--reset', action="store_true", help="Reset the chatminer configurations to default values")
@milc.cli.subcommand("Set a chatminer configuration item, using dot notation\nExample: 'chatminer set-config -n database.password -v myPassword'")
def configure(cli: milc.MILC) -> None:
    if cli.args.reset:
        config.reset_configs()
    else:
        name = cli.args.name if cli.args.name else missing_arg("Config item name is required")
        value = cli.args.value if cli.args.value else missing_arg("Config item value is required")
        config.set_config(name, value)


@milc.cli.subcommand("Removes all files and databases persisted by chatminer on the local system")
def uninstall(cli: milc.MILC) -> None:
    config.delete_configs()
    sqlitedb.delete_database()


def missing_arg(arg_name: str) -> None:
    error(f"{arg_name} is required!")
    exit(1)


def main() -> None:
    milc.cli()
