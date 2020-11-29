from slydb import *

lexer = CmdLexer()
parser = CmdParser()
print("R")
parser.parse(lexer.tokenize("R := inputfromfile(sales)"))
parser.parse(lexer.tokenize("R"))
print("R1")
parser.parse(lexer.tokenize("R1 := select(R, (time > 50) and (qty < 30))"))
parser.parse(lexer.tokenize("R1"))
parser.parse(lexer.tokenize("outputtofile(R1, bar)"))
print("R8")
parser.parse(lexer.tokenize("R8 := select(R, time > 50)"))
parser.parse(lexer.tokenize("R8"))
print("R9")
parser.parse(lexer.tokenize("R9 := select(R, pricerange = \"outrageous\")"))
parser.parse(lexer.tokenize("R9"))
print("R2")
parser.parse(lexer.tokenize("R2 := project(R1, saleid, qty, customerid, pricerange)"))
parser.parse(lexer.tokenize("R2"))
print("R3")
parser.parse(lexer.tokenize("R3 := avg(R1, qty)"))
parser.parse(lexer.tokenize("R3"))
print("R4")
parser.parse(lexer.tokenize("R4 := sumgroup(R1, time, qty)"))
parser.parse(lexer.tokenize("R4"))
print("R5")
parser.parse(lexer.tokenize("R5 := sumgroup(R1, qty, time, pricerange)"))
parser.parse(lexer.tokenize("R5"))
print("R6")
parser.parse(lexer.tokenize("R6 := avggroup(R1, qty, pricerange)"))
parser.parse(lexer.tokenize("R6"))


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
