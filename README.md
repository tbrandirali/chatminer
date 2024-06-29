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
Because of this, chatminer only supports loading exports from WhatsApp mobile.
Before running chatminer, extract the `.txt` file from the `.zip` archive.

WhatsApp exports include chat notifications, such as:
"_Alice changed their phone number to a new number_" or
"_Your security code with Bob changed_."
Chatminer tries to filter these out with a hardcoded list of standard notifications,
but this list is probably incomplete.

Since WhatsApp does not properly escape messages and contact names,
there are edge cases in which chatminer may not accurately parse messages or filter notifications.
For example, since WhatsApp does not escape newlines in exports, 
a line in the file could be either a new message or a continuation of the previous one.
Chatminer attempts to fix it by detecting whether lines start with a timestamp, but this approach has limits.

Consider the following text as a message content (notice the line break):
```
This is an example of what lines in a WhatsApp chat export look like
1/01/20, 12:00 - Alice: This is a message
```

In a chat export, since WhatsApp does not escape newlines, that would look like:
```
1/01/20, 12:00 - Bob: This is an example of what lines in a WhatsApp chat export look like
1/01/20, 12:00 - Alice: This is a message
```

That is completely ambiguous. There is no sure way to tell whether the second line is a separate message
or a continuation of the content of the previous one, and so chatminer will parse it as a separate message.

Chat notifications also introduce unavoidable ambiguity, 
largely revolving around the possibility of contact names containing colons.

For example, this line:
```
1/01/20, 12:00 - Alice: pinned a message
```

could be a message by `Alice` saying she pinned a message, 
or it could be a notification saying that a contact named `Alice:` (with the colon) pinned a message.
Chatminer would parse it as a notification.

In general, messages which accidentally fit notification patterns will be parsed as notifications.
For a list of the notification patterns see [parser.py](chatminer/parser.py).

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
(supports optional keyword filtering like the previous command):

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