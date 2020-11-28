import numpy as np

"""
函数和类的设计，参考SQL语法和pandas
https://www.w3school.com.cn/sql/index.asp
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html#pandas.DataFrame.query
python类的override
https://docs.python.org/zh-cn/3/reference/datamodel.html#special-method-names
"""


class Table:
    def __init__(self, col_names):
        self.cols = {}
        self.rows = np.empty([0, len(col_names)])
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
        return

    def select(self, columns):
        return

    def query(self,query):



