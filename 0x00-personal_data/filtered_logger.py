#!/usr/bin/env python3
"""
Task

3. Connect to secure database

Database credentials should NEVER be stored in code or checked into version
control. One secure option is to store them as environment variable on the
application server.

In this task, you will connect to a secure holberton database to read a users
table. The database is protected by a username and password that are set as
environment variables on the server named PERSONAL_DATA_DB_USERNAME (set the
default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default as an empty
string) and PERSONAL_DATA_DB_HOST (set the default as “localhost”).

The database name is stored in PERSONAL_DATA_DB_NAME.

Implement a get_db function that returns a connector to the database
(mysql.connector.connection.MySQLConnection object).

Use the os module to obtain credentials from the environment
Use the module mysql-connector-python to connect to the MySQL database
(pip3 install mysql-connector-python)
"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates message with redaction"""
    for f in fields:
        repl = f + '=' + redaction + separator
        message = re.sub((f + '=.*?' + separator), repl, message)
    return message


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger after setting the properties according to the
    specification
    """
    user_data = logging.getLogger("user_data")
    user_data.propagate = False
    user_data.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    user_data.addHandler(handler)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database using environment variables
    for credentials.
    Returns a MySQLConnection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    cnx = mysql.connector.connect(user=username, password=password, host=host,
                                  database=db_name)
    return cnx


def main() -> None:
    """
    """
    pass


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum
        """
        filtered_msg = filter_datum(self._fields, self.REDACTION, record.msg,
                                    self.SEPARATOR)
        record.msg = filtered_msg
        return super().format(record)
