#!/usr/bin/env python3
"""
Module to filter PII data fields from log records.
"""

import re

def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specific fields in a log message.

    Args:
        fields (list): List of fields to obfuscate.
        redaction (str): The value to obfuscate the fields with.
        message (str): The log message.
        separator (str): Field separator in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f"{field}=[^;]*", f"{field}={redaction}", message)
    return message
