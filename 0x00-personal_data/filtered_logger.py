#!/usr/bin/env python3
"""
Task

1. Log formatter

Update the RedactingFormatter class to accept a list of strings fields
constructor argument.

Implement the format method to filter values in incoming log records using
filter_datum. Values for fields in fields should be filtered.

DO NOT extrapolate FORMAT manually. The format method should be less than 5
lines long.
"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates message with redaction, to mask the fields in the fields list
    """
    for field in fields:
        repl = field + '=' + redaction + separator
        message = re.sub(field + '=.*?' + separator, repl, message)
    return message


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
        print("Result of filtered_msg is {}".format(filtered_msg))
        return super().format(record)
