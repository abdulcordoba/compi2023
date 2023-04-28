from antlr4 import CommonTokenStream, FileStream

from antlr.ExprLexer import ExprLexer
from antlr.ExprParser import ExprParser


def main():
    fs = FileStream('input.txt')
    lexer = ExprLexer(fs)
    ts = CommonTokenStream(lexer)
    parser = ExprParser(ts)

    cst = parser.prog()

    print(cst)


if __name__ == '__main__':
    main()