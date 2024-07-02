import milc

from chatminer import commands, common


@milc.cli.entrypoint('This is chatminer! Specify a command to use...')
def entrypoint(cli: milc.MILC) -> None:
    common.log('No subcommand specified!')


@milc.cli.argument('-i', '--input', help="Input text file")
@milc.cli.argument('-c', '--chat', help="The name to give to the imported chat")
@milc.cli.subcommand('Import a whatsapp chat as txt file into an SQL table')
def create(cli: milc.MILC) -> None:
    file_path = cli.args.input if cli.args.input else missing_arg("Input file path is required")
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")
    commands.create(file_path, chat_name)


@milc.cli.argument('-c', '--chat', help="The name of the chat to delete")
@milc.cli.subcommand('Delete the database table for an imported chat')
def delete(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")
    commands.delete(chat_name)


@milc.cli.argument('-c', '--chat', help="The chat name to plot frequency for")
@milc.cli.argument('-k', '--keyword', help="A keyword to plot the frequency of in the given chat")
@milc.cli.subcommand('Plot the message frequency over time for a specific chat')
def frequency(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")
    keyword = cli.args.keyword
    commands.frequency(chat_name, keyword)


@milc.cli.argument('-c', '--chat', help="The chat name to plot frequency for")
@milc.cli.argument('-k', '--keyword', help="A keyword to plot the frequency of in the given chat")
@milc.cli.subcommand('Plot the message frequency over time for each sender in a specific chat')
def frequency_per_sender(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")
    keyword = cli.args.keyword
    commands.frequency_per_sender(chat_name, keyword)


@milc.cli.argument('-c', '--chat', help="The chat name to show notifications for")
@milc.cli.subcommand('Print all the notifications for a chat')
def notifications(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")
    commands.notifications(chat_name)


@milc.cli.argument('-c', '--chat', help="The chat name to show a summary for")
@milc.cli.subcommand('Print a summary of statistics for a chat')
def senders(cli: milc.MILC) -> None:
    chat_name = cli.args.chat if cli.args.chat else missing_arg("Chat name is required")
    commands.senders(chat_name)


@milc.cli.subcommand("Removes all files and databases persisted by chatminer on the local system")
def uninstall(cli: milc.MILC) -> None:
    commands.uninstall()


def missing_arg(arg_name: str) -> None:
    common.error(f"{arg_name} is required!")
    exit(1)


def main() -> None:
    milc.cli()


if __name__ == "__main__":
    main()
