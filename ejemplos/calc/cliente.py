from antlr4 import *
from antlr.ExprLexer import ExprLexer
from antlr.ExprParser  import ExprParser
from antlr.ExprListener import ExprListener
import sys

r = []
def cast(x): return lambda: int(x)
def mult(x, y): return lambda: x()*y()
def div(x, y): return lambda: x()/y()
def add(x, y): return lambda: x()+y()
def sub(x, y): return lambda: x()-y()

class KeyPrinter(ExprListener):     
    def exitMult(self, ctx):         
        r.append(mult(r.pop(), r.pop()))

    def exitAdd(self, ctx):         
        r.append(add(r.pop(), r.pop()))

    def exitDiv(self, ctx):
        y = r.pop()
        x = r.pop()
        r.append(div(x, y))

    def exitSub(self, ctx):         
        y = r.pop()
        x = r.pop()
        r.append(sub(x, y))

    def exitInt(self, ctx):
        r.append(cast(ctx.INT().getText()))

def main(argv):
    input = FileStream("ejemplo.txt")
    lexer = ExprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.prog()
    printer = KeyPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    print (r[0])
    print (r[0]())

if __name__ == '__main__':
    main(sys.argv)
