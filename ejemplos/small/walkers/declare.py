INT = 0
BOOL = 1

from small.SmallListener import SmallListener
from .env import Env

class DeclareListener(SmallListener):
    def __init__(self):
        self.declaring = -1
        self.env = Env()
        self.types = {}

    def getTypes(self):
        return self.types

    def enterIntDecl(self, ctx):
        self.declaring = INT

    def exitIntDecl(self, ctx):
        self.declaring = -1

    def enterBoolDecl(self, ctx):
        self.declaring = BOOL

    def exitBoolDecl(self, ctx):
        self.declaring = -1

    def enterIdent_list(self, ctx):
        for x in ctx.ident():
            self.env.declare(x.ID().getText(), self.declaring)

    def exitId(self, ctx):
        type = self.env.getType(ctx.ID().getText())
        self.types[ctx] = type
