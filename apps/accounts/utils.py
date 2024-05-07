"""
Contains utility functions related to accounts app.
"""
import re


def validate_password_format(password: str) -> bool:
    """
    Validate format of a password.

    :param password: password to be validated.
    :return: True if password is valid, False otherwise.
    """
    res = re.match(r"^[a-zA-Z0-9!\"#$%&'()*+,-./:;<>?=@[\\\]^_`{|}~]+$", password)
    return bool(res)
