import re

import numpy as np


class Table:
    def __init__(self, col_names):
        self.cols = {}
        self.rows = np.empty([0, len(col_names)])
        self.rows_number = 0
        self.col_names = np.array(col_names)
        for col_idx, col_name in enumerate(col_names):
            self.cols[col_name] = col_idx

    def to_csv(self, file, sep=","):
        with open(file, "a") as f:
            f.write(sep.join(self.col_names))
            f.write("\n")
            for i in range(0, len(self.rows)):
                f.write(sep.join(self.rows[i]))
                f.write("\n")

    def print(self, sep=",", **kwargs):
        for idx, value in enumerate(self.col_names):
            if idx != 0:
                print("%s" % sep, end='')
            print(value, end='')
        print("")
        for i in range(0, len(self.rows)):
            for idx, value in enumerate(self.rows[i]):
                if idx != 0:
                    print("%s" % sep, end='')
                print(value, end='')
            print("")

    def insert(self, row):
        # 插入行
        self.rows = np.concatenate((self.rows, [row]), axis=0)
        self.rows_number += 1

    def query(self, query: str):
        # TODO
        rows = self.rows[np.where(query)]
        return rows

    def __getitem__(self, key):
        return self.rows[key]
