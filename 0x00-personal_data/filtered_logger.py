#!/usr/bin/env python3
"""
Task

4. Read and filter data

Implement a main function that takes no arguments and returns nothing.

The function will obtain a database connection using get_db and retrieve all
rows in the users table and display each row under a filtered format like this:

[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***;
phone=***; ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b;
last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0 (compatible; MSIE 9.0;
Windows NT 6.1; WOW64; Trident/5.0; KTXN);
Filtered fields:

    - name
    - email
    - phone
    - ssn
    - password
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
    Obtain a database connection using get_db and retrieve all rows in the
    users table and display each row under a filtered format
    """
    cnx = get_db()
    curA = cnx.cursor()
    curA.execute("SELECT * FROM users")
    for (name, email, phone, ssn, password, ip, last_login,
         user_agent) in curA:
        message = (
            "name={};email={};phone={};ssn={};password={};ip={};last_login={};\
                    user_agent={};".format(name, email, phone, ssn, password,
                                           ip, last_login, user_agent))
        logger = get_logger()
        logger.log(logging.INFO, message)


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


if __name__ == "__main__":
    main()
