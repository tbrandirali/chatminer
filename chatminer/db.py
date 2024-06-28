import psycopg
from psycopg import sql

from chatminer.common import log, error
from chatminer.config import configs
from chatminer.model.message import Message
from chatminer.model.notification import Notification


def db_exists(conn: psycopg.Connection, db_name: str) -> bool:
    with conn.cursor() as cursor:
        query = sql.SQL("SELECT EXISTS (SELECT {column} FROM {table} WHERE {column} = %s)").format(
            table=sql.Identifier('pg_database'),
            column=sql.Identifier('datname'),
        )
        cursor.execute(query, (db_name,))
        return cursor.fetchall()[0][0]


def create_conn(db_name: str, autocommit: bool = False) -> psycopg.Connection:
    host = configs['database']['host']
    user = configs['database']['user']
    password = configs['database']['password']
    pwd_suffix = f":{password}" if password else ""
    return psycopg.connect(
        f"postgresql://{user}{pwd_suffix}@{host}:5432/{db_name}",
        autocommit=autocommit
    )


def create_db(conn: psycopg.Connection) -> None:
    exists = db_exists(conn, configs['database']['name'])
    with conn.cursor() as cursor:
        if exists:
            log("Database 'chatminer' already exists")
        else:
            query = sql.SQL("CREATE DATABASE {db_name}").format(
                db_name=sql.Identifier(configs['database']['name'])
            )
            cursor.execute(query)
            if cursor.statusmessage == "CREATE DATABASE":
                log("Database 'chatminer' created")
            else:
                raise RuntimeError("Database 'chatminer' does not exist and could not be created")


def delete_db(conn: psycopg.Connection) -> None:
    with conn.cursor() as cursor:
        query = sql.SQL("DROP DATABASE IF EXISTS {db_name}").format(
            db_name=sql.Identifier(configs['database']['name'])
        )
        cursor.execute(query)
        log(cursor.statusmessage)
        if cursor.statusmessage == "DROP DATABASE":
            log("Database 'chatminer' deleted")
        else:
            raise RuntimeError("Error deleting database")


def create_messages_table(conn: psycopg.Connection, table_name: str) -> None:
    with conn.cursor() as cursor:
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                sender TEXT NOT NULL,
                text TEXT NOT NULL
            )
        """).format(
            table_name=sql.Identifier(table_name)
        )
        cursor.execute(query)
        if cursor.statusmessage == "CREATE TABLE":
            log(f"Database table '{table_name}' created")
        else:
            raise RuntimeError(f"Table {table_name} does not exist and could not be created")


def create_notifications_table(conn: psycopg.Connection, table_name: str) -> None:
    with conn.cursor() as cursor:

        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                text TEXT NOT NULL
            )
        """).format(
            table_name=sql.Identifier(table_name)
        )
        cursor.execute(query)
        if cursor.statusmessage == "CREATE TABLE":
            log(f"Database table '{table_name}' created")
        else:
            raise RuntimeError(f"Table {table_name} does not exist and could not be created")


def delete_table(conn: psycopg.Connection, table_name: str) -> None:
    with conn.cursor() as cursor:
        query = sql.SQL("""
            DROP TABLE {table_name}
        """).format(
            table_name=sql.Identifier(table_name)
        )
        cursor.execute(query)
        if cursor.statusmessage == "DROP TABLE":
            log(f"Database table {table_name} deleted")
        else:
            log(f"delete_table statusmessage: {cursor.statusmessage}")
            raise RuntimeError(f"Table {table_name} could not be deleted")


def insert_messages(conn: psycopg.Connection, table_name: str, messages: list[Message]) -> None:
    with conn.cursor() as cursor:
        insert_query = f"""
            INSERT INTO {table_name} (id, time, sender, text) 
                VALUES (%s, %s, %s, %s)
        """
        for message in messages:
            cursor.execute(insert_query, [message.id, message.time, message.sender, message.text])
        log(f"Added {len(messages)} new messages")


def insert_notifications(conn: psycopg.Connection, table_name: str, notifications: list[Notification]) -> None:
    with conn.cursor() as cursor:
        insert_query = f"""
            INSERT INTO {table_name} (id, time, text) 
                VALUES (%s, %s, %s)
        """
        for notification in notifications:
            cursor.execute(insert_query, [notification.id, notification.time, notification.text])
        log(f"Added {len(notifications)} new notifications")


def get_all_messages(conn: psycopg.Connection, table_name: str) -> list[Message]:
    with conn.cursor() as cursor:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
    messages = [Message(id, time, sender, text) for id, time, sender, text in results]
    return messages
