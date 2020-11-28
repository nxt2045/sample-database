# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 Double ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。




# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
if __name__ == '__main__':
    lexer = CommandLexer()
    parser = CommandParser()
    while True:
        try:
            text = input('>> ')
        except EOFError:
            break
        if text:
            # for tok in lexer.tokenize(text):
            #    print(tok)
            parser.parse(lexer.tokenize(text))
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
