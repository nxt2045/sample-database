from tree import BPlusTree
from copy import deepcopy
from hash import Hash
import operator

COMP_FUNC = {
    "<": operator.lt, ">": operator.gt, "=": operator.eq, "!=": operator.ne,
    ">=": operator.ge, "<=": operator.le
}
R_COMP = {
    ">": "<", "<": ">", "=": "=", "!=": "!=",
    "<=": ">=", ">=": "<="
}


def read_csv(file_name, sep='|'):
    file = open(file_name, 'r')
    col_names = [x for x in next(file).strip().split(sep)]
    lines = [line.rstrip() for line in file]
    file.close()
    lines = [line for line in lines if line]
    data = [list(map(int, line.split(sep))) for line in lines]
    table = Table(col_names=col_names, data=data)
    return table


def join(table1, table2, condition):
    # make sure table1 < table2, else swap
    if len(table1.data) < len(table2.data):
        pass
    else:
        table1, table2 = table2, table1
        condition = [condition[2], R_COMP[condition[1]], condition[0]]
    index1 = table1.cols[condition[0]]
    index2 = table2.cols[condition[2]]
    col_names = table1.col_names + table2.col_names
    result = []
    if condition[0] in table1.idxs:
        for i in range(0, len(table2.data)):
            row1_idxs = table1.idxs[condition[0]].range_search(condition[1], int(table2.data[i][index2]))
            row1 = [table1.data[idx] for idx in row1_idxs]
            row2 = list(table2.data[i])
            for j in range(0, len(row1)):
                result.append(row1[j] + row2)
    elif condition[2] in table2.idxs:
        for i in range(0, len(table1.data)):
            row2_idxs = table2.idxs[condition[0]].range_search(condition[1], int(table1.data[i][index1]))
            row2 = [table2.data[idx] for idx in row2_idxs]
            row1 = list(table1.data[i])
            for j in range(0, len(row2)):
                result.append(row1 + row2[j])
    else:
        for i in range(0, len(table2.data)):
            comp_func = COMP_FUNC[condition[1]]
            row1 = [row for row in table1.data if comp_func(row[index1], int(table2.data[i][index2]))]
            row2 = list(table2.data[i])
            for j in range(0, len(row1)):
                result.append(row1[j] + row2)
    table = Table(col_names=col_names, data=result)
    return table


def concat(table1, table2):
    result = table1.data
    for i in table2.data:
        result.append(i)
    table = Table(col_names=table1.col_names, data=result)
    return table


class Table:
    def __init__(self, col_names, data, idxs=None, idx_type=None):
        self.col_names = col_names[:]
        self.cols = {}
        for col_index, col_name in enumerate(col_names):
            self.cols[col_name] = col_index
        self.data = data
        # copy speed: https://www.geeksforgeeks.org/python-cloning-copying-list/
        # self.data = [] if not data else [row[:] for row in data]
        self.idxs = {} if not idxs else {k: v for k, v in idxs.items}
        self.idx_type = {} if not idx_type else {k: v for k, v in idx_type.items}

    def __str__(self, gap=14):
        print(" ", end='')
        for i in self.col_names:
            print(i.ljust(gap), end='')
        print("")
        row_idxs = range(min(len(self.data), 2))
        # row_idxs=range(len(self.data))
        for i in row_idxs:
            print(" ", end='')
            for j in self.data[i]:
                print(str(j).ljust(gap), end='')
            print("")
        return "[" + str(len(self.data)) + " rows and " + str(len(self.col_names)) + " columns]"

    def select(self, condition):
        if not condition[2].isdigit():  # not int
            j1 = self.cols[condition[0]]
            j2 = self.cols[condition[2]]
            comp_func = COMP_FUNC[condition[1]]
            data = [row for row in self.data if comp_func(row[j1], row[j2])]
        elif condition[0] in self.idxs:  # int and ids
            row_idxs = self.idxs[condition[0]].range_search(condition[1], int(condition[2]))
            data = [self.data[idx] for idx in row_idxs]
        else:  # int not idx
            j1 = self.cols[condition[0]]
            comp_func = COMP_FUNC[condition[1]]
            data = [row for row in self.data if comp_func(row[j1], int(condition[2]))]
        return Table(col_names=self.col_names, data=data)

    def project(self, Clist):
        result = [["0"] * len(Clist) for i in range(len(self.data))]
        for i in range(0, len(self.data)):
            for j in range(0, len(Clist)):
                index = self.cols[Clist[j]]
                result[i][j] = self.data[i][index]
        return Table(col_names=Clist, data=result)

    def sum(self, C1):
        j1 = self.cols[C1]
        data = [[sum([row[j1] for row in self.data])]]
        return Table(col_names=['sum(' + C1 + ')'], data=data)

    def avg(self, C1):
        j1 = self.cols[C1]
        data = [[sum([row[j1] for row in self.data]) / len(self.data)]]
        return Table(col_names=['avg(' + C1 + ')'], data=data)

    def sumgroup(self, C1, Clist):
        group_dic = {}
        j1s = [self.cols[C] for C in Clist]
        for i in range(0, len(self.data)):
            key = ''
            value_list = []
            group_list = []
            for j1 in j1s:
                key += str(self.data[i][j1])
                group_list.append(self.data[i][j1])
            if key in group_dic.keys():
                value_list = group_dic[key]
                value_list[1] += self.data[i][self.cols[C1]]
                group_dic[key] = value_list
            else:
                value_list.append(group_list)
                value_list.append(self.data[i][self.cols[C1]])
                group_dic[key] = value_list
        result = []
        for i in group_dic.values():
            temp = i[0]
            temp.append(i[1])
            result.append(temp)
        Clist.append("sum")
        table = Table(col_names=Clist, data=result)
        return table

    def avggroup(self, C1, Clist):
        group_dic = {}
        for i in range(0, len(self.data)):
            key = ''
            value_list = []
            group_list = []
            for j in Clist:
                index = self.cols[j]
                key += str(self.data[i][index])
                group_list.append(self.data[i][index])
            if key in group_dic.keys():
                value_list = group_dic[key]
                value_list[1] += self.data[i][self.cols[C1]]
                value_list[2] += 1
                group_dic[key] = value_list
            else:
                value_list.append(group_list)
                value_list.append(self.data[i][self.cols[C1]])
                value_list.append(1)
                group_dic[key] = value_list
        result = []
        for i in group_dic.values():
            temp = i[0]
            i[1] = i[1] / i[2]
            temp.append(i[1])
            result.append(temp)
        Clist.append("avg")
        table = Table(col_names=Clist, data=result)
        return table

    def add_prefix(self, NAME):
        col_names = [NAME + self.col_names[i] for i in range(len(self.col_names))]
        idxs = {NAME + k: v for k, v in self.idxs.items()}
        idx_type = {NAME + k: v for k, v in self.idx_type.items()}
        table = Table(col_names=col_names, data=self.data, idxs=idxs, idx_type=idx_type)
        return table

    def movavg(self, C1, k):
        table = Table(col_names=self.col_names, data=deepcopy(self.data))
        # table = Table(col_names=self.col_names, data=self.data)
        j1 = self.cols[C1]
        table.col_names[j1] = 'movavg(' + table.col_names[j1] + ')'
        for i in range(0, len(self.data)):
            count = 0
            sum = 0
            for j in range(i, -1, -1):
                if count == int(k):
                    break
                count += 1
                sum += self.data[j][j1]
            table.data[i][j1] = sum / count
        return table

    def movsum(self, C1, k):
        table = Table(col_names=self.col_names, data=deepcopy(self.data))
        # table = Table(col_names=self.col_names, data=self.data)
        j1 = self.cols[C1]
        table.col_names[j1] = 'movavg(%s)' % table.col_names[j1]
        for i in range(0, len(self.data)):
            count = 0
            sum = 0
            for j in range(i, -1, -1):
                if count == int(k):
                    break
                count += 1
                sum += self.data[j][j1]
            table.data[i][j1] = sum
        return table

    def sort(self, C1):
        if len(self.data) <= 1:
            result = self.data
        elif C1 in self.idxs and self.idx_type == "BTREE":
            j1s = self.idxs[C1].values()
            result = [self.data[j1] for j1 in j1s]
        else:
            j1 = self.cols[C1]
            less = self.select((C1, "<", str(self.data[1][j1])))
            more = self.select((C1, ">", str(self.data[1][j1])))
            equal = self.select((C1, "=", str(self.data[1][j1])))
            less = less.sort(C1)
            more = more.sort(C1)
            result = []
            for x in (less, equal, more):
                for i in range(len(x.data)):
                    result.append(x.data[i])
        table = Table(col_names=self.col_names, data=result)
        return table

    def set_index(self, C1, index_type):
        j1 = self.cols[C1]
        model = BPlusTree(32) if index_type == "BTREE" else Hash()
        for i in range(0, len(self.data)):
            model.insert(self.data[i][j1], i)
        self.idxs[C1], self.idx_type[C1] = model, index_type

    def to_txt(self, file_name, sep="|"):
        with open(file_name, "w") as f:
            f.write(sep.join(self.col_names) + "\n")
            for i in range(0, len(self.data)):
                f.write(str(self.data[i]).replace(",", sep)[1:-1] + "\n")
