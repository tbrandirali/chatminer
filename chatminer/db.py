import sqlite3
import shutil
from datetime import datetime
from typing import Iterable

from platformdirs import PlatformDirs
from pathlib import Path

from chatminer.common import log, error
from chatminer.model.message import Message
from chatminer.model.notification import Notification

db_path = Path(PlatformDirs("chatminer").user_data_dir) / 'chatminer.db'


def create_connection() -> sqlite3.Connection:
    if not db_path.parent.is_dir():
        db_path.parent.mkdir(exist_ok=True, parents=True)
    return sqlite3.connect(db_path)


def create_messages_table(conn: sqlite3.Connection, table_name: str) -> None:
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            sender TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    log(f"Database table '{table_name}' created")


def create_notifications_table(conn: sqlite3.Connection, table_name: str) -> None:
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            text TEXT NOT NULL
        )
    """)
    log(f"Database table '{table_name}' created")


def delete_table(conn: sqlite3.Connection, table_name: str) -> None:
    conn.execute(f"""
        DROP TABLE {table_name}
    """)
    log(f"Database table {table_name} deleted")


def insert_messages(conn: sqlite3.Connection, table_name: str, messages: Iterable[Message]) -> None:
    i = 0
    for message in messages:
        conn.execute(f"""
            INSERT INTO {table_name} (id, time, sender, text) 
                VALUES (?, ?, ?, ?)
        """, [message.id, message.time, message.sender, message.text])
        i += 1
    log(f"Added {i} new messages")


def insert_notifications(conn: sqlite3.Connection, table_name: str, notifications: Iterable[Notification]) -> None:
    i = 0
    for notification in notifications:
        conn.execute(f"""
            INSERT INTO {table_name} (id, time, text) 
                VALUES (?, ?, ?)
        """, [notification.id, notification.time, notification.text])
        i += 1
    log(f"Added {i} new notifications")


def get_all_messages(conn: sqlite3.Connection, chat_name: str) -> list[Message]:
    try:
        cursor = conn.cursor()
        results = cursor.execute(f"SELECT * FROM {chat_name}").fetchall()
        return [
            Message(id, datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), sender, text)
            for id, time, sender, text in results
        ]
    except sqlite3.OperationalError as err:
        if "no such table:" in str(err):
            error(f"Chat '{chat_name}' not found")
            exit(1)
        else:
            raise err


def get_all_notifications(conn: sqlite3.Connection, chat_name: str) -> list[Notification]:
    try:
        cursor = conn.cursor()
        results = cursor.execute(f"SELECT * FROM {chat_name}_notifications").fetchall()
        return [
            Notification(id, datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), text)
            for id, time, text in results
        ]
    except sqlite3.OperationalError as err:
        if "no such table:" in str(err):
            error(f"Chat '{chat_name}' not found")
            exit(1)
        else:
            raise err


def delete_database() -> None:
    if db_path.parent.is_dir():
        shutil.rmtree(db_path.parent)
        log("Database file deleted")
    else:
        log("No database file found to delete")
