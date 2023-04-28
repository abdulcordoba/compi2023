from antlr4 import *
from antlr.SmallLexer import SmallLexer
from antlr.SmallParser import SmallParser
from antlr.SmallListener import SmallListener
from walkers.declare import DeclareListener
from walkers.typecheck import TypecheckListener
import sys


class TreePrinter(SmallListener):
    pass


def main(argv):
    parser = SmallParser(CommonTokenStream(SmallLexer(FileStream(argv[1]))))
    tree = parser.program()
    declarations = DeclareListener()

    walker = ParseTreeWalker()
    walker.walk(declarations, tree)
    typecheck = TypecheckListener(declarations.getTypes())
    walker.walk(typecheck, tree)


if __name__ == '__main__':
    main(sys.argv)
