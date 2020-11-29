from .table import Table


def read_csv(path, sep):
    with open(path, 'r') as file:
        lines = [line.rstrip() for line in file.readlines()]  # nxt: include blank line
        rows = [line for line in lines if line]  # nxt: non blank line
    if len(rows) != 0:
        col_names = rows[0].split("|")
        table = Table(col_names)
    else:
        raise Exception()
    for i in range(1, len(rows)):
        table.insert(rows[i].split("|"))
    return table


def join(t1_name, t1: Table, t2_name, t2: Table, query):
    # todo
    # create new table with appropriate name and columns
    t1_col_names = [t1_name + "_" + x for x in t1.col_names]
    t2_col_names = [t2_name + "_" + x for x in t2.col_names]
    table = Table(t1_col_names + t2_col_names)
    return table

def project(table:Table, col_names):
    col_idxs = [table.cols[col_name] for col_name in col_names]
    rows = table[:, col_idxs]
    table = Table(col_names)
    for i in range(len(rows)):
        table.insert(rows[i])
    return table

