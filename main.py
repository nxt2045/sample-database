from slydb import *

lexer = CmdLexer()
parser = CmdParser()
while True:
    try:
        text = input('>> ')
    except EOFError:
        break
    if text:
        # for tok in lexer.tokenize(text):
        #    print(tok)
        parser.parse(lexer.tokenize(text))