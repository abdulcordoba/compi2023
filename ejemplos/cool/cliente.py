from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from antlr.coolListener import coolListener
import sys


class MyListener(coolListener):
    def enterAttribute(self, ctx:coolParser.AttributeContext):
        if ctx.ID().getText() == 'self':
            raise Exception('Error: self usado como nombre de variable')


def main(argv):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(argv))))
    tree = parser.program()

    myListener = MyListener()

    walker = ParseTreeWalker()
    walker.walk(myListener, tree)


if __name__ == '__main__':
    main('../../resources/semantic/input/anattributenamedself.cool')
