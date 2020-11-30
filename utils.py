from table import Table
import numpy as np


def read_csv(path, sep):
    with open(path, 'r') as file:
        lines = [line.rstrip() for line in file.readlines()]  # Note: include blank line
        rows = [line for line in lines if line]  # Note: non blank line
    if len(rows) != 0:
        col_names = rows[0].split(sep)
    else:
        raise Exception()
    if len(rows) > 1:
        table = Table(col_names=col_names, data=[rows[i].split("|") for i in range(1, len(rows))])
    else:
        table = Table(col_names=col_names)
    return table


def project(table: Table, col_names: list):
    data = table[col_names]  # define by __getitem__ func
    table = Table(col_names=col_names, data=data)
    return table
