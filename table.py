import re
from typing import Type, List, Any

import numpy as np
from io import StringIO


class Table:
    def __init__(self, col_names: List[str], data=None):
        self.cols = {}
        self.rows = {}
        self.col_dtypes = {}
        self.col_names = col_names
        for col_idx, col_name in enumerate(col_names):
            self.cols[col_name] = col_idx
        if type(data) == np.ndarray or data:
            self.matrix = np.array(data)
            self.update_dtypes()
        else:
            self.matrix = np.empty([0, len(self.col_names)])

    def to_csv(self, path, sep=","):
        with open(path, "w") as f:
            f.write(sep.join(self.col_names))
            f.write("\n")
            for i in range(0, len(self.matrix)):
                f.write(sep.join(self.matrix[i]))
                f.write("\n")

    def __get_dtype(self, words):
        def is_dtype(words, dtype):
            try:
                for w in words:
                    dtype(w)
                return True
            except ValueError:
                return False

        data_types = [int, float, str]
        for data_type in data_types:
            if is_dtype(words, data_type):
                return data_type
        return str

    def update_dtypes(self):
        if self.matrix.shape[0] == 0:
            pass
        else:
            for col_idx, col_name in enumerate(self.col_names):
                data = self.matrix[:, col_idx].flatten()
                self.col_dtypes[col_name] = self.__get_dtype(data)

    def insert(self, data):
        # 插入行
        data = np.array(data)
        if len(data.shape) == 1:
            self.matrix = np.concatenate((self.matrix, [data]))
        elif len(data.shape) == 2:
            self.matrix = np.concatenate((self.matrix, data))

    def query(self, query: str):
        new_matrix = np.empty([0, len(self.col_names)])
        used_col_names = [col_name for col_name in self.col_names if query.find(col_name) != -1]
        used_col_idx = [self.cols[used_col_name] for used_col_name in used_col_names]
        for row in self.matrix:
            for (col_idx, col_name) in zip(used_col_idx, used_col_names):
                value = row[col_idx]
                if self.col_dtypes[col_name] == str:
                    value = "\"" + value + "\""
                exec('{} = {}'.format(col_name, value))
            if eval(query):
                new_matrix = np.concatenate((new_matrix, [row]))
        table = Table(self.col_names)
        for i in range(new_matrix.shape[0]):
            table.insert(new_matrix[i])
        table.update_dtypes()
        return table

    def __getitem__(self, key):
        # overwrite []
        if type(key) == str:
            # table['A']
            col_idx = self.cols[key]
            row = self.matrix[:, col_idx].flatten()
            return row.astype(self.__get_dtype(row))
        elif type(key) == list:
            # table[['A','B','C']]
            col_idx = [self.cols[i] for i in key]
            return self.matrix[:, col_idx]

    def __str__(self, sep=", "):
        # overwrite print
        output = ""
        for idx, value in enumerate(self.col_names):
            if idx != 0:
                output += sep
            output += str(value)
        output += "\n"
        for i in range(0, len(self.matrix)):
            for idx, value in enumerate(self.matrix[i]):
                if idx != 0:
                    output += sep
                output += str(value)
            output += "\n"
        return output.strip("\n")
