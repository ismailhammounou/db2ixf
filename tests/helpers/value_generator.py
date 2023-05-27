# coding=utf-8
"""Value generator"""
import random
import string
from datetime import datetime

random.seed(1991)


def random_date(date_format: str = None) -> str:
    """Generate a random date.

    Returns
    -------
    str:
        Random date.
    """
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    if random.randint(0, 20) == 0:
        return ""
    end = datetime(2019, 1, 1).timestamp()
    epoch = random.random() * end
    return datetime.fromtimestamp(epoch).strftime(date_format)


def random_string(max_length: int = 30) -> str:
    """Generate a random string with a known maximal length.

    Parameters
    ----------
    max_length : int
        Maximal length of the string.

    Returns
    -------
    str:
        Random string.
    """
    if random.randint(0, 20) == 0:
        return ""
    letters_ = string.ascii_letters + "éàè'î" + " "
    return "".join([random.choice(letters_) for _ in range(random.randint(1, max_length))])


def random_int() -> str:
    """Generate a random integer as a string.

    Returns
    -------
    str:
        Random integer.
    """
    if random.randint(0, 20) == 0:
        return ""
    return "{:d}".format(random.randint(0, 1000))


def random_double() -> str:
    """Generate a random double as a string.
    Returns
    -------
    str:
        Random double.
    """
    if random.randint(0, 20) == 0:
        return ""
    return str(round(random.uniform(0.0, 1000.0), 6))


def random_boolean() -> str:
    """Generate a random boolean as a string
    Returns
    -------
    str:
        Random boolean.
    """
    return "True" if random.getrandbits(1) else "False"
