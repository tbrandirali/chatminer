# A CLI tool to analyse your WhatsApp chats

Chatminer allows you to import your WhatsApp chats from exported `.txt` files 
into database tables, and then lets you query and plot various statistics for them.

Chatminer currently depends on an external instance of Postgres for the database.
Database connection info can be specified using chatminer commands.

## Usage

Import a new chat from a `.txt` file.

```bash
chatminer create -i "path/to/chat_file.txt" -c "chat_name"
```

Plot the overall frequency of messages for a chat.

```bash
chatminer plot-freq -c "chat_name"
```

Plot the frequency of messages containing a specific keyword for a chat.
The keyword can be a full regex expression.

```bash
chatminer plot-freq -c "chat_name" -k "keyword"
```

Plot the frequency of messages for each sender in a chat.
This command supports keyword filtering like the previous one.

```bash
chatminer plot-freq-per-sender -c "chat_name" -k "keyword"
```

Delete an imported chat.

```bash
chatminer delete -c "chat_name"
```

On every run chatminer checks for the existence of its config file;
if it does not exist then it creates one with defaults, 
and if it does then it reads the configurations for this run from it.

By default chatminer assumes it is using a local database, 
running as an admin user with username "_postgres_" and no password.
If the setting `database.admin` is set to _True_, chatminer will try to create 
its own database with the name given in `database.name` (defaults to "chatminer"),
if it doesn't already exist. If it's not running as admin then it expects a database
with the configured name to already exist.

Set persistent configuration options.

```bash
chatminer set-config -n "database.host" -v "localhost"
```

Reset chatminer's config file to its default values.

```bash
chatminer set-config -r
```

Uninstall chatminer: remove files persisted by it and databases created 
in its current configuration.

```bash
chatminer uninstall
```