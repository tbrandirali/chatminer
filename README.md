# A CLI tool to analyse your WhatsApp chats

Chatminer allows you to import your WhatsApp chats from exported `.txt` files 
into database tables, and then lets you query and plot various statistics for them.

## Installation

You can install chatminer using pip:

```bash
pip install git+https://github.com/tbrandirali/chatminer.git@main
```

## WhatsApp export files

Whatsapp desktop does not load the entire chat history, 
so the chat exports from desktop will be incomplete.
Also, the message format in the desktop exports is different from the mobile ones.
Because of this chatminer only supports loading exports from WhatsApp mobile.
Before running chatminer, extract the `.txt` file from the `.zip` archive.

## Usage

Import a new chat from a `.txt` file:

```bash
chatminer create -i "path/to/chat_file.txt" -c "chat_name"
```

Plot the overall frequency of messages for a chat:

```bash
chatminer frequency -c "chat_name"
```

Plot the frequency of messages containing a specific keyword for a chat 
(the keyword can be a full regex expression):

```bash
chatminer frequency -c "chat_name" -k "keyword"
```

Plot the frequency of messages for each sender in a chat
(supports keyword filtering like the previous command):

```bash
chatminer frequency-per-sender -c "chat_name" -k "keyword"
```

Delete an imported chat:

```bash
chatminer delete -c "chat_name"
```

Uninstall chatminer, remove database files and folders created by it:

```bash
chatminer uninstall
```