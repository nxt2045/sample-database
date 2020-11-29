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

def join(table0,table1, query):
    # create new table with appropriate name and columns
    t1_cols = [tables[0] + "_" + x for x in t1.col_names]
    t2_cols = [tables[1] + "_" + x for x in t2.col_names]
    table = Table(out_table_name, t1_cols + t2_cols)

    join = Join(t1, t2, criteria)
    data = join.do_join()
    table.set_data(data)
    self.__save_table(out_table_name, table)
    # table.print()
    print("%d rows returned" % len(data))
    return True
]



