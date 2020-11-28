from sly import Lexer, Parser
from .table import *
import numpy as np

"""
https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer
 CommandLexer: break up the input cmd into "tokens".
     strings that correspond to the "base case" symbols used in required grammar. 
     These are keywords, such as "select" or "create"; 
     punctuation and relation symbols such as "()," ">=<"; 
     and other _database (of columns or tables);
"""


class CmdLexer(Lexer):
    """
    the basic operations of relational algebra:
    selection, projection, join, group by, sum, average aggregates
    """
    tokens = {INPUT, OUTPUT, SELECT, PROJECT, AVGGROUP, AVG, SUMGROUP, SORT, JOIN, MOVAVG, MOVSUM, CONCAT, BTREE, HASH, COMP, OR, AND, NAME, NUMBER, DEFINE}
    literals = {'(', ')', ',', '"'}
    # nxt: regular expression rules for tokens
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
    # nxt: ignore space and tab characters between tokens
    ignore = ' \t'
    # nxt: other ignored expression
    ignore_comment = r'//.*'
    ignore_newline = r'\n+'

    # nxt: tracking命令行数
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1