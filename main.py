#!/usr/bin/env python3
from database import read_csv, join, concat
from sly import Lexer, Parser
import time


class MyLexer(Lexer):
    tokens = {INPUT, OUTPUT, SELECT, PROJECT, AVGGROUP, AVG, SUMGROUP, SUM, SORT, JOIN, MOVAVG, MOVSUM, CONCAT, BTREE, HASH, COMP, OR, AND, NAME, NUMBER, DEFINE}
    literals = {'(', ')', ',', '"'}
    ignore = ' \t'

    # Tokens
    INPUT = r'inputfromfile'
    OUTPUT = r'outputtofile'
    SELECT = r'select'
    PROJECT = r'project'
    AVGGROUP = r'avggroup'
    AVG = r'avg'
    SUMGROUP = r'sumgroup'
    SORT = r'sort'
    JOIN = r'join'
    MOVAVG = r'movavg'
    MOVSUM = r'movsum'
    CONCAT = r'concat'
    BTREE = r'Btree'
    HASH = r'Hash'
    COMP = r'[><=!]+'
    OR = r'or'
    AND = r'and'
    NAME = r'[\']?[a-zA-Z_./][a-zA-Z0-9_./]*[\']?'
    NUMBER = r'\d+'
    DEFINE = r':='


    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class MyParser(Parser):
    """
    @_('statements statements')
    def statements(self, p):
        return p.statement + [ p.statememts ]
    """
    tokens = MyLexer.tokens

    def __init__(self):
        self.names = {}

    @_('NAME DEFINE expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr
        print(self.names[p.NAME])

    @_('expr')
    def statement(self, p):
        if p.expr in self.names:
            print(self.names[p.expr])
        else:
            print(p.expr)

    @_('HASH "(" NAME "," expr ")"')
    def statement(self, p):
        self.names[p.NAME].set_index(p.expr, "HASH")

    @_('BTREE "(" NAME "," expr ")"')
    def statement(self, p):
        self.names[p.NAME].set_index(p.expr, "BTREE")

    @_('OUTPUT "(" NAME "," NAME ")"')
    def statement(self, p):
        self.names[p.NAME0].to_txt(p.NAME1, sep='|')

    @_('INPUT "(" NAME ")"')
    def expr(self, p):
        return read_csv(p.NAME, sep='|')

    @_('SELECT "(" NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME].select(p.expr)

    @_('JOIN "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        df0 = self.names[p.NAME0].add_prefix(p.NAME0 + "_")
        df1 = self.names[p.NAME1].add_prefix(p.NAME1 + "_")
        query = list(p.expr)
        for i in range(0, len(query)):
            query[i] = query[i].replace(".", "_")
        return join(df0, df1, query)

    @_('PROJECT "(" NAME "," expr ")"')
    def expr(self, p):
        new_expr = p.expr if type(p.expr) == list else [p.expr]
        return self.names[p.NAME].project(new_expr)

    @_('AVG "(" NAME "," NAME ")"')
    def expr(self, p):
        return self.names[p.NAME0].avg(p.NAME1)

    @_('SUM "(" NAME "," NAME ")"')
    def expr(self, p):
        return self.names[p.NAME0].sum(p.NAME1)

    @_('SUMGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        new_expr = p.expr if type(p.expr) == list else [p.expr]
        return self.names[p.NAME0].sumgroup(p.NAME1, new_expr)

    @_('AVGGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        new_expr = p.expr if type(p.expr) == list else [p.expr]
        return self.names[p.NAME0].avggroup(p.NAME1, new_expr)

    @_('SORT "(" NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME].sort(p.expr)

    @_('MOVAVG "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        k = p.NUMBER
        return self.names[p.NAME0].movavg(p.NAME1, k)

    @_('MOVSUM "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        k = p.NUMBER
        return self.names[p.NAME0].movsum(p.NAME1, k)

    @_('CONCAT "(" NAME "," NAME ")"')
    def expr(self, p):
        return concat(self.names[p.NAME0], self.names[p.NAME1])

    @_('"(" expr ")" OR "(" expr ")"')
    def expr(self, p):
        return p.expr0 + " or " + p.expr1

    @_('"(" expr ")" AND "(" expr ")"')
    def expr(self, p):
        return p.expr0 + " and " + p.expr1;

    @_('NAME COMP NAME')
    def expr(self, p):
        return p.NAME0, p.COMP, p.NAME1

    @_('NAME COMP "\"" NAME "\""')
    def expr(self, p):
        return p.NAME0 + p.COMP + "\"" + p.NAME1 + "\""

    @_('NAME COMP NUMBER')
    def expr(self, p):
        return p.NAME, p.COMP, p.NUMBER

    @_('NAME "," expr')
    def expr(self, p):
        new_expr = [p.NAME].extend(p.expr) if type(p.expr) == list else [p.NAME, p.expr]
        return new_expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return p.NAME


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    while True:
        try:
            text = input(' pd >> ')
        except EOFError:
            break
        if text:
            start_time = time.time()
            parser.parse(lexer.tokenize(text))
            end_time = time.time()
            print("total time: " + str(end_time - start_time))
