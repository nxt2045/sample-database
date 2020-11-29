from slydb import *

lexer = CmdLexer()
parser = CmdParser()

parser.parse(lexer.tokenize("R := inputfromfile(sales)"))
print("R1")
parser.parse(lexer.tokenize("R1 := select(R, (time > 50) and (qty < 30))"))
parser.parse(lexer.tokenize("R1"))
parser.parse(lexer.tokenize("outputtofile(R1, bar)"))
print("R8")
parser.parse(lexer.tokenize("R8 := select(R, time > 50)"))
parser.parse(lexer.tokenize("R8"))




"""
while True:
    try:
        text = input('>> ')
    except EOFError:
        break
    if text:
        # for tok in lexer.tokenize(text):
        #    print(tok)
        parser.parse(lexer.tokenize(text))
"""
