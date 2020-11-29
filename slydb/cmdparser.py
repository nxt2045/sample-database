from sly import Lexer, Parser
from .table import *
from .cmdlexer import *
import numpy as np
from typing import Dict, Type, Set, Union, Tuple
from .operations import *
from .table import Table

"""
https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer
CommandParser: execrate tokens
    consists of a set of functions that can call each other recursively, 
    to operate on the sequence of tokens, for example:
        @_('statements statements')
        def statements(self, p):
    p: YaccProduction object, {token, matched cmd}
    everytime use "p.expr", match func statement again.
"""


class CmdParser(Parser):
    tokens = CmdLexer.tokens

    def __init__(self):
        self._tables = {}

    # recursively run statement
    @_('NAME DEFINE expr')
    def statement(self, p):
        self._tables[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        if p.expr in self._tables:
            # eg: R
            self._tables[p.expr].print(sep=", ")
        else:
            print(p.expr)

    @_('INPUT "(" NAME ")"')
    def expr(self, p):
        return read_csv(p.NAME, sep='|')

    @_('OUTPUT "(" NAME "," NAME ")"')
    def statement(self, p):
        self._tables[p.NAME0].to_csv(p.NAME1, sep='|')

    @_('HASH "(" NAME "," expr ")"')
    @_('BTREE "(" NAME "," expr ")"')
    def statement(self, p):
        self._tables[p.NAME] = self._tables[p.NAME].reset_index()
        self._tables[p.NAME] = self._tables[p.NAME].set_index(p.expr)
        self._tables[p.NAME] = self._tables[p.NAME].sort_index()

    @_('SELECT "(" NAME "," expr ")"')
    def expr(self, p):
        # 分析见README.md
        return self._tables[p.NAME].query(p.expr)

    @_('JOIN "(" NAME "," NAME "," expr ")"')
    # eg: T1 := join(R1, S, R1.qty <= S.Q)
    def expr(self, p):
        """
        pandas:
        df0 = self._tables[p.NAME0].add_prefix(p.NAME0 + "_")
        df1 = self._tables[p.NAME1].add_prefix(p.NAME1 + "_")
        query = p.expr.replace(".", "_")
        return pandas.merge(df0.assign(key=0), df1.assign(key=0), on='key').drop('key', axis=1).query(query)
        """
        return join(p.NAME0, self._tables[p.NAME0], p.NAME1, self._tables[p.NAME1], p.expr)

    @_('PROJECT "(" NAME "," expr ")"')
    def expr(self, p):
        l = p.expr
        if type(l) != list:
            l = [p.expr]
        return project(self._tables[p.NAME], col_names=l)

    @_('AVG "(" NAME "," NAME ")"')
    def expr(self, p):
        return self._tables[p.NAME0][p.NAME1].mean()

    @_('SUMGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        return self._tables[p.NAME0].groupby(p.expr)[p.NAME1].sum()

    @_('AVGGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        return self._tables[p.NAME0].groupby(p.expr)[p.NAME1].mean()

    @_('SORT "(" NAME "," expr ")"')
    def expr(self, p):
        return self._tables[p.NAME].sort_values(by=p.expr)

    @_('MOVAVG "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return self._tables[p.NAME0][p.NAME1].rolling(int(p.NUMBER), min_periods=1).mean()
        # df[col].rolling(num,min_periods=1).mean()

    @_('MOVSUM "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return self._tables[p.NAME0][p.NAME1].rolling(int(p.NUMBER), min_periods=1).sum()

    @_('CONCAT "(" NAME "," NAME ")"')
    def expr(self, p):
        return pandas.concat([self._tables[p.NAME0], self._tables[p.NAME1]])

    # nxt: OR = r'or'
    @_('"(" expr ")" OR "(" expr ")"')
    def expr(self, p):
        # nxt: "or" is python operator or
        return p.expr0 + " or " + p.expr1

    # nxt: AND = r'and'
    @_('"(" expr ")" AND "(" expr ")"')
    def expr(self, p):
        # nxt: "and" is python operator and
        return p.expr0 + " and " + p.expr1

    # The comparators for select and join will be =, <, >, !=, >=, <=.
    @_('NAME COMP NAME')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME0 + "==" + p.NAME1
            # return p.NAME0+"=="+"\""+p.NAME1+"\""
        else:
            return p.NAME0 + p.COMP + p.NAME1
            # return p.NAME0+p.COMP+"\""+p.NAME1+"\""

    @_('NAME COMP "\"" NAME "\""')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME0 + "==" + "\"" + p.NAME1 + "\""
        else:
            return p.NAME0 + p.COMP + "\"" + p.NAME1 + "\""

    @_('NAME COMP NUMBER')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME + "==" + p.NUMBER
        else:
            return p.NAME + p.COMP + p.NUMBER

    @_('NAME "," expr')
    def expr(self, p):
        l = [p.NAME]
        if type(p.expr) == list:
            l.extend(p.expr)
        else:
            l.append(p.expr)
        return l

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return p.NAME
