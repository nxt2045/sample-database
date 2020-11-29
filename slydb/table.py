import re
from typing import Type, List

import numpy as np
from io import StringIO


class Table:

    def __init__(self, col_names):
        self.cols = {}
        self.rows = {}
        self.col_types = []
        self.matrix = np.empty([0, len(col_names)])
        self.col_names = np.array(col_names)
        for col_idx, col_name in enumerate(col_names):
            self.cols[col_name] = col_idx

    def to_csv(self, file, sep=","):
        with open(file, "a") as f:
            f.write(sep.join(self.col_names))
            f.write("\n")
            for i in range(0, len(self.matrix)):
                f.write(sep.join(self.matrix[i]))
                f.write("\n")

    def set_col_types(self, row):
        def is_int(word):
            try:
                int(word)
                return True
            except ValueError:
                return False

        def is_float(word):
            try:
                float(word)
                return True
            except ValueError:
                return False

        self.col_types = [str] * len(row)
        for i in range(len(row)):
            print(i, row[i])
            if is_int(row[i]):
                self.col_types[i] = int
            elif is_float(row[i]):
                self.col_types[i] = float
            else:  # return as string
                self.col_types[i] = str

    def print(self, sep=",", **kwargs):
        for idx, value in enumerate(self.col_names):
            if idx != 0:
                print("%s" % sep, end='')
            print(value, end='')
        print("")
        for i in range(0, len(self.matrix)):
            for idx, value in enumerate(self.matrix[i]):
                if idx != 0:
                    print("%s" % sep, end='')
                print(value, end='')
            print("")

    def insert(self, row):
        # 插入行
        self.matrix = np.concatenate((self.matrix, [row]))

    def select(self, query: str):
        new_matrix = np.empty([0, len(self.col_names)])
        for row in self.matrix:
            for col_idx, col_name in enumerate(self.col_names):
                value = row[col_idx]
                if self.col_types[col_idx] == str:
                    value = "\"" + value + "\""
                exec('{} = {}'.format(col_name, value))
            if eval(query):
                new_matrix = np.concatenate((new_matrix, [row]))
        return new_matrix

    def __getitem__(self, key):
        return self.matrix[key]
