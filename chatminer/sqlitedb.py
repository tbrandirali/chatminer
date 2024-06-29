import sqlite3
import shutil
from datetime import datetime

from chatminer.config import configs
from chatminer.common import log
from chatminer.model.message import Message
from chatminer.model.notification import Notification


def create_connection() -> sqlite3.Connection:
    return sqlite3.connect(configs['database']['path'])


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


def insert_messages(conn: sqlite3.Connection, table_name: str, messages: list[Message]) -> None:
    for message in messages:
        conn.execute(f"""
            INSERT INTO {table_name} (id, time, sender, text) 
                VALUES (?, ?, ?, ?)
        """, [message.id, message.time, message.sender, message.text])
    log(f"Added {len(messages)} new messages")


def insert_notifications(conn: sqlite3.Connection, table_name: str, notifications: list[Notification]) -> None:
    for notification in notifications:
        conn.execute(f"""
            INSERT INTO {table_name} (id, time, text) 
                VALUES (?, ?, ?)
        """, [notification.id, notification.time, notification.text])
    log(f"Added {len(notifications)} new notifications")


def get_all_messages(conn: sqlite3.Connection, table_name: str) -> list[Message]:
    cursor = conn.cursor()
    results = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
    return [
        Message(id, datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), sender, text)
        for id, time, sender, text in results
    ]


def delete_database() -> None:
    shutil.rmtree(configs['database']['path'])
    log("Database file deleted")
