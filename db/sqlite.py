import sqlite3
import typing

import config


def dict_factory(cursor, row):
    """It converts raw tuple-based records into a dict object"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    conn: typing.Union[sqlite3.Connection] = None
    cursor: typing.Union[sqlite3.Cursor]

    def __init__(self):
        self.open(config.Database.DB_NAME)

    def migrate(self):
        """Migrate creates non-existing tables in the given database"""
        self.cursor.execute(
            "PRAGMA foreign_keys = ON;"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (uuid VARCHAR(128) NOT NULL PRIMARY KEY, "
            "username VARCHAR(24) NOT NULL UNIQUE, hashed_password VARCHAR(128) NOT NULL, "
            "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, access_token VARCHAR(128) NOT NULL, "
            "refresh_token VARCHAR(128) NOT NULL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_uuid VARCHAR(128) NOT NULL, text VARCHAR(256) NOT NULL, "
            "published_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, deleted_at TIMESTAMP DEFAULT NULL,"
            "FOREIGN KEY (user_uuid) REFERENCES users (uuid))"
        )
        self.conn.commit()

    def open(self, db_name: str):
        try:
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.conn.row_factory = dict_factory
        except sqlite3.Error as e:
            print("Error connecting to database! Error: ", e.__str__())

    def fetch(self, query: str, many: bool = False) -> typing.Union[typing.List[dict], dict, None]:
        with self:
            self.cursor.execute(query)
            tx = self.cursor.fetchone() if not many else self.cursor.fetchall()
            return tx

    def execute(self, query: str, parameters: typing.Iterable = None):
        with self:
            self.cursor.execute(query, parameters)

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
