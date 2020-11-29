from .table import Table
import numpy as np
from io import StringIO

"""
do database level function
"""


def read_csv(path, sep):
    with open(path, 'r') as file:
        lines = [line.rstrip() for line in file.readlines()]  # Note: include blank line
        rows = [line for line in lines if line]  # Note: non blank line
    if len(rows) != 0:
        col_names = rows[0].split(sep)
        table = Table(col_names)
    else:
        raise Exception()
    if len(rows) > 1:
        table.set_col_types(rows[1].split("|"))
        for i in range(1, len(rows)):
            table.insert(rows[i].split("|"))
    return table


class SlyDB:
    def __init__(self):
        self._tables = {}

    def add(self, name, table: Table):
        self._tables[name] = table

    def get(self, name):
        return self._tables[name]

    def join(self, t1_name, t2_name, query):
        # TODO:
        # create new table with appropriate name and columns
        t1 = self._tables[t1_name]
        t2 = self._tables[t2_name]
        t1_col_names = [t1_name + "_" + x for x in t1.col_names]
        t2_col_names = [t2_name + "_" + x for x in t2.col_names]
        # ...
        table = Table(t1_col_names + t2_col_names)
        return table

    def select(self, name: str, query: str):
        # TODO
        table = self._tables[name]
        matrix = table.select(query)
        table = Table(table.col_names)
        for i in range(matrix.shape[0]):
            table.insert(matrix[i])
        return table


    def project(self, name: str, col_names):
        table = self._tables[name]
        col_idxs = [table.cols[col_name] for col_name in col_names]
        rows = table[:, col_idxs]
        table = Table(col_names)
        for i in range(len(rows)):
            table.insert(rows[i])
        return table
