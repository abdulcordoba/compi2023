from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from antlr.coolListener import coolListener
from structure import setBaseKlasses, SymbolTable, Klass, lookupClass, Method, SymbolTableWithScopes
import sys

class ClassesFirstPass(coolListener):
    """
    Se requiere hacer una primera pasada revisando todas las clases que se van a definir,
    aquí solamente captura esos nombres y la clase de la cual hereda, es necesario porque la clase de la que
    se hereda posiblemente sea declarada después.
    """
    def enterKlass(self, ctx:coolParser.KlassContext):
        """
        El constructor Klass además registra las clases en el registro global (ver allClasses en structure.py)
        """
        if ctx.TYPE(1):
            Klass(ctx.TYPE(0).getText(), ctx.TYPE(1).getText())
        else:
            Klass(ctx.TYPE(0).getText())

class ClassDeclarations(coolListener):
    """
    En esta clase ya se hace la declaración de features de la clase (atributos y métodos)
    """
    def enterKlass(self, ctx:coolParser.KlassContext):
        """
        La clase ya debe existir en el registro, entonces la tomo en una variable para después
        en qué clase voy (ver recorrido en el árbol)
        """
        self.currentKlass = lookupClass(ctx.TYPE(0).getText())

    def enterAttribute(self, ctx:coolParser.AttributeContext):
        """
        Declaración de un atributo, uso la clase activa en este recorrido
        """
        self.currentKlass.addAttribute(ctx.ID().getText(), lookupClass(ctx.TYPE().getText()))

    def enterMethod(self, ctx:coolParser.MethodContext):
        """
        Declaración de un método, también uso la clase activa en este recorrido, solo que el también debo
        de guardar los parámetros, ver addMethod en structure.py
        """
        r = []
        for p in ctx.params:
            r.append(  (p.ID().getText(), p.TYPE().getText()) )
        self.currentKlass.addMethod(ctx.ID().getText(), Method(lookupClass(ctx.TYPE().getText()), r))

class TypeChecker(coolListener):
    """
    Esta clase se va a encargar de hacer la validación de tipos. Normalmente, en las expresiones, se usan los
    métodos exitXXXXX para garantizar que los hijos en el árbol ya hayan sido recorridos. Se usa una tabla de
    símbolos que tiene scopes para a) clase (atributos) b) métodos c) locales con let
    """

    def enterKlass(self, ctx:coolParser.KlassContext):
        """
        La tabla queda activa por clase, por eso la uso como parámetro: para tener visibilidad de los atributos
        """
        self.table = SymbolTableWithScopes(lookupClass(ctx.TYPE(0).getText()))

    def enterMethod(self, ctx:coolParser.MethodContext):
        """
        Aquí se abre el scope para los parámetros del método (y se guardan en la tabla)
        """
        self.table.openScope()
        self.letscopes = 0 # será usado más tarde, es para las locales
        for f in ctx.params:
            self.table[f.ID().getText()] = lookupClass(f.TYPE().getText())

    def exitMethod(self, ctx:coolParser.MethodContext):
        """
        Cerrar el scope de método
        """
        self.table.closeScope()

    def enterLet_decl(self, ctx:coolParser.Let_declContext):
        """
        La declaración de variables locales es mediante el let_decl, pero tengo que guardar cuántos
        scopes han sido creados para después eliminarlos.
        """
        self.table.openScope()
        self.table[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())
        self.letscopes = self.letscopes + 1

    def exitLet(self, ctx:coolParser.LetContext):
        """
        Aquí se destruyen los scopes del let
        """
        while self.letscopes:
            self.table.closeScope()
            self.letscopes = self.letscopes - 1

    def exitPri(self, ctx:coolParser.PriContext):
        """
        El tipo de las expresiones primarias está determinado por su hijo, ver línea 22 del cool.g4, y luego
        la regla 53 donde vienen literales, paréntesis y uso de variable.
        """
        ctx.type = ctx.primary().type

    def exitParens(self, ctx:coolParser.ParensContext):
        """
        Los paréntesis solamente toman el tipo de su subexpresión para asignarlo a este nodo
        """
        ctx.type = ctx.expr().type

    def exitInt(self, ctx:coolParser.IntContext):
        """
        Los nodos entero de inmediato asignan su tipo al nodo
        """
        ctx.type = lookupClass('Int')

    def exitStr(self, ctx:coolParser.StrContext):
        """
        Los nodos string de inmediato asignan su tipo al nodo
        """
        ctx.type = lookupClass('String')

    def exitBool(self, ctx:coolParser.BoolContext):
        """
        Los nodos boolean de inmediato asignan su tipo al nodo
        """
        ctx.type = lookupClass('Bool')

    def exitVar(self, ctx:coolParser.VarContext):
        """
        Los nodos variable toman su tipo de la tabla (buscan el tipo con el que fueron definidos)
        """
        ctx.type = self.table[ctx.ID().getText()]


def main(argv):
    # Crear el frontend
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(argv))))
    # Ejecutar el parsing llamando a la primera regla en la gramática
    tree = parser.program()
    # Aquí definimos de manera global las clases peredefinidas en Cool (ver el método en structure.py)
    setBaseKlasses()

    # De aquí en adelante se llaman los visitors definidos arriba
    walker = ParseTreeWalker()
    walker.walk(ClassesFirstPass(), tree)
    walker.walk(ClassDeclarations(), tree)
    walker.walk(TypeChecker(), tree)

    # Llego hasta aquí solamente en el caso de que no se halla encontrado error
    print("No hay errores semánticos en el programa.")


if __name__ == '__main__':
    main('../../resources/semantic/input/baddispatch.cool')
