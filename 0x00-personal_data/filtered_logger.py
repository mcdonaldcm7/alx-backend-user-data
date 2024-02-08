#!/usr/bin/env python3
"""
Task

0. Regex-ing

Write a function called filter_datum that returns the log message obfuscated:

    - Arguments:
        * fields: a list of strings representing all fields to obfuscate
        * redaction: a string representing by what the field will be obfuscated
        * message: a string representing the log line
        * separator: a string representing by which character is separating all
        fields in the log line (message)
    - The function should use a regex to replace occurrences of certain field
    values.
    - filter_datum should be less than 5 lines long and use re.sub to perform
    the substitution with a single regex.
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """
    Obfuscates message with redaction, to mask the fields in the fields list
    """
    for field in fields:
        pattern = field + '=.*?' + seperator
        repl = field + '=' + redaction + seperator
        message = re.sub(pattern, repl, message)
    return message
