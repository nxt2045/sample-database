import re

import numpy as np

class Table:
    def __init__(self, col_names):
        self.cols = {}
        self.rows = np.empty([0, len(col_names)])
        self.rows_number = 0
        self.col_names = np.array([col_names])
        for col_idx, col_name in enumerate(col_names):
            self.cols[col_name] = col_idx

    def to_csv(self, file, sep=","):
        with open(file, "a") as f:
            self.print(file, sep)

    def print(self, file, sep=",", **kwargs):
        for idx, name in enumerate(self.col_names):
            if idx != 0:
                print(" %s " % sep, end='', file=file)
            print(name, end='', file=file)
        for i in range(0, len(self.rows)):
            for idx, value in enumerate(self.rows[i]):
                if idx != 0:
                    print(" %s " % sep, end='', file=file)

    def insert(self, row):
        self.rows = np.concatenate((self.rows, row))
        self.rows_number += 1

    def query(self, query: str):
        # todo
        rows = self.rows[np.where(query)]
        return rows




