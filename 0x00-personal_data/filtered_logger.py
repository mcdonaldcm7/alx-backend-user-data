#!/usr/bin/env python3
"""
Task

2. Create logger

Implement a get_logger function that takes no arguments and returns a
logging.Logger object.

The logger should be named "user_data" and only log up to logging.INFO level.
It should not propagate messages to other loggers. It should have a
StreamHandler with RedactingFormatter as formatter.

Create a tuple PII_FIELDS constant at the root of the module containing the
fields from user_data.csv that are considered PII. PII_FIELDS can contain only
5 fields - choose the right list of fields that can are considered as
“important” PIIs or information that you must hide in your logs. Use it to
parameterize the formatter.
"""
from typing import List
import re
import logging


PII_FIELDS = ("email", "phone", "ssn", "ip", "password")


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
