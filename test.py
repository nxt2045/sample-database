from main import MyLexer, MyParser
import time

lexer = MyLexer()
parser = MyParser()
with open('docs/test-all.txt', 'r') as file:
    lines = [line.rstrip() for line in file.readlines()]  # All lines including the blank ones
    commands = [line for line in lines if line and line[0] != "#" and line[0] != "/"]  # Non-blank lines
for i in range(len(commands)):
    if commands[i]:
        text = commands[i]
        print("\n[%d] pd >> %s" % (int(i + 1), text))
        start_time = time.time()
        parser.parse(lexer.tokenize(text))
        end_time = time.time()
        print("total time: " + str(end_time - start_time))