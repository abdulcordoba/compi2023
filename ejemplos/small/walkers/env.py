class AlreadyDeclaredException(Exception):
    pass

class NotDeclaredException(Exception):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return "La variable %s no fue declarada" % self.var

class Env():
    def __init__(self):
        self.rep = {}
    def declare(self, symbol, type):
        if symbol in self.rep.keys():
            raise AlreadyDeclaredException()
        else:
            self.rep[symbol] = type

    def getType(self, symbol):
        if not symbol in self.rep.keys():
            for i in self.rep.keys():
                print(i)
            raise NotDeclaredException(symbol)
        else:
            return self.rep[symbol]