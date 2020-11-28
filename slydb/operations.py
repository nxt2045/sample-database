from .table import Table
def read_csv(path, sep):
    with open(p.NAME, 'r') as file:
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

def tablize(table,col_names):
    return table.select(col_names)




