#!/usr/bin/env python3
import pandas as pd
from sly import Lexer, Parser
from utils import *

"""
https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer
 CommandLexer: break up the input cmd into "tokens".
     strings that correspond to the "base case" symbols used in required grammar. 
     These are keywords, such as "select" or "create"; 
     punctuation and relation symbols such as "()," ">=<"; 
     and other _database (of columns or tables);
"""


class MyLexer(Lexer):
    tokens = {INPUT, OUTPUT, SELECT, PROJECT, AVGGROUP, AVG, SUMGROUP, SORT, JOIN, MOVAVG, MOVSUM, CONCAT, BTREE, HASH, COMP, OR, AND, NAME, NUMBER, DEFINE}
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
    COMP = r'[><=]+'
    OR = r'or'
    AND = r'and'
    NAME = r'[\']?[a-zA-Z_][a-zA-Z0-9_.]*[\']?'
    NUMBER = r'\d+'
    DEFINE = r':='
    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class MyParser(Parser):
    '''
    @_('statements statements')
    def statements(self, p):
        return p.statement + [ p.statememts ]
    '''
    tokens = MyLexer.tokens
    # debugfile = 'parser.out'

    def __init__(self):
        self.names = {}

    @_('NAME DEFINE expr')
    def statement(self, p):
        # print("NAME DEFINE expr")
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        # print("expr")
        if p.expr in self.names:
            print(self.names[p.expr])
        else:
            print(p.expr)

    @_('HASH "(" NAME "," expr ")"')
    @_('BTREE "(" NAME "," expr ")"')
    def statement(self, p):
        self.names[p.NAME] = self.names[p.NAME].reset_index()
        self.names[p.NAME] = self.names[p.NAME].set_index(p.expr)
        self.names[p.NAME] = self.names[p.NAME].sort_index()

    @_('OUTPUT "(" NAME "," NAME ")"')
    def statement(self, p):
        self.names[p.NAME0].to_csv(p.NAME1, sep='|')

    @_('INPUT "(" NAME ")"')
    def expr(self, p):
        return read_csv(p.NAME, sep='|')

    @_('SELECT "(" NAME "," expr ")"')
    def expr(self, p):
        # print('SELECT "(" NAME "," expr ")"')
        return self.names[p.NAME].query(p.expr)

    @_('JOIN "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        # print('JOIN "(" NAME "," NAME "," expr ")"')
        df0 = self.names[p.NAME0].add_prefix(p.NAME0 + "_")
        df1 = self.names[p.NAME1].add_prefix(p.NAME1 + "_")
        query = p.expr.replace(".", "_")
        return pd.merge(df0.assign(key=0), df1.assign(key=0), on='key').drop('key', axis=1).query(query)

    @_('PROJECT "(" NAME "," expr ")"')
    def expr(self, p):
        l = p.expr
        if type(l) != list:
            l = [p.expr]
        return project(self.names[p.NAME], col_names=l)

    @_('AVG "(" NAME "," NAME ")"')
    def expr(self, p):
        return self.names[p.NAME0][p.NAME1].mean()

    @_('SUMGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME0].groupby(p.expr)[p.NAME1].sum()

    @_('AVGGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME0].groupby(p.expr)[p.NAME1].mean()

    @_('SORT "(" NAME "," expr ")"')
    def expr(self, p):
        return self.names[p.NAME].sort_values(by=p.expr)

    @_('MOVAVG "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return self.names[p.NAME0][p.NAME1].rolling(int(p.NUMBER), min_periods=1).mean()

    @_('MOVSUM "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return self.names[p.NAME0][p.NAME1].rolling(int(p.NUMBER), min_periods=1).sum()

    @_('CONCAT "(" NAME "," NAME ")"')
    def expr(self, p):
        return pd.concat([self.names[p.NAME0], self.names[p.NAME1]])

    @_('"(" expr ")" OR "(" expr ")"')
    def expr(self, p):
        # print('"(" expr ")" OR "(" expr ")"')
        return p.expr0 + " or " + p.expr1;

    @_('"(" expr ")" AND "(" expr ")"')
    def expr(self, p):
        # print('"(" expr ")" AND "(" expr ")"')
        return p.expr0 + " and " + p.expr1;

    @_('NAME COMP NAME')
    def expr(self, p):
        # print('NAME COMP NAME')
        if p.COMP == "=":
            return p.NAME0 + "==" + p.NAME1
            # return p.NAME0+"=="+"\""+p.NAME1+"\""
        else:
            return p.NAME0 + p.COMP + p.NAME1
            # return p.NAME0+p.COMP+"\""+p.NAME1+"\""

    @_('NAME COMP "\"" NAME "\""')
    def expr(self, p):
        # print('NAME COMP "\"" NAME "\""')
        if p.COMP == "=":
            return p.NAME0 + "==" + "\"" + p.NAME1 + "\""
        else:
            return p.NAME0 + p.COMP + "\"" + p.NAME1 + "\""

    @_('NAME COMP NUMBER')
    def expr(self, p):
        # print('NAME COMP NUMBER')
        if p.COMP == "=":
            return p.NAME + "==" + p.NUMBER
        else:
            return p.NAME + p.COMP + p.NUMBER

    @_('NAME "," expr')
    def expr(self, p):
        # print('NAME "," expr')
        l = [p.NAME]
        if type(p.expr) == list:
            l.extend(p.expr)
        else:
            l.append(p.expr)
        return l

    @_('"(" expr ")"')
    def expr(self, p):
        # print('"(" expr ")"')
        return p.expr

    @_('NAME')
    def expr(self, p):
        # print('NAME')
        return p.NAME


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    test_mode = "auto"  # auto
    if test_mode == "input":
        while True:
            try:
                text = input('pd >> ')
            except EOFError:
                break
            if text:
                # for tok in lexer.tokenize(text):
                #    print(tok)
                parser.parse(lexer.tokenize(text))
    elif test_mode == "auto":
        lexer = MyLexer()
        parser = MyParser()
        with open('test.txt', 'r') as file:
            lines = [line.rstrip() for line in file.readlines()]  # All lines including the blank ones
            commands = [line for line in lines if line]  # Non-blank lines
        for i in range(len(commands)):
            if commands[i]:
                text = commands[i]
                print("\n[%d] pd >> %s" % (int(i + 1), text))
                # for token in lexer.tokenize(text):
                #     print("\t", token)
                parser.parse(lexer.tokenize(text))
