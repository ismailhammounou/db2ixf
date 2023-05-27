# coding=utf-8
"""Data generator will help to create data that will be use in the creation of a spark dataframe."""
from typing import List, Tuple
from .value_generator import (
    random_date, random_boolean, random_double, random_int, random_string
)

random_functions = {
    0: random_int,
    1: random_string,
    2: random_date,
    3: random_boolean,
    4: random_double,
}


def create_dataframe_data(number_lines: int = 10, cols: List[str] = None) -> Tuple:
    """Create pyspark dataframe data.

     Parameters
     ----------
     number_lines : int
         Number of lines we want to create in the dataframe.
     cols : List[str]
         List of columns.

     Returns
     -------
     Tuple :
         2-tuples with the list of generated data and the list of columns.
    """
    if cols is None:
        cols = [f"C{i + 1}" for i in range(5)]
    number_cols = len(cols)
    lines = []
    for _ in range(number_lines):
        line = ()
        for i in range(number_cols):
            line = (random_functions[i % 5](), *line)
        lines.append(line)
    return lines, cols
