from small.SmallListener import SmallListener

INT = 0
BOOL = 1

class TypeException(Exception):
    pass

class TypecheckListener(SmallListener):
    def __init__(self, types):
        self.types = types

    def exitNot(self, ctx):
        if self.types[ctx.getChild(1)] != BOOL:
            raise TypeException()
        else:
            self.types[ctx] = BOOL

    def exitTrue(self, ctx):
        self.types[ctx] = BOOL

    def exitFalse(self, ctx):
        self.types[ctx] = BOOL

    def exitAssign(self, ctx):
        type1 = self.types[ctx.getChild(0)]
        type2 = self.types[ctx.getChild(2)]
        if type1 != type2:
            raise TypeException()
