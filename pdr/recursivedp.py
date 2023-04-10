"""
Parser descendente recursivo para la sintaxis de expresiones aritméticas.

Este tipo de parser es PREDICTIVO.
Tiene problemas con:
    Recursión izquierda
    Reglas factorizables por la izquierda
    Reconocimiento de épsilon/lambda

Gramática original (¿por qué el orden de rhs?):

E -> E + T
E -> E - T
E -> T
T -> T * F
T -> T / F
T -> F
F -> (E)
F -> literal

Sin recursión izquierda:

E  -> T E'
E' -> + T E'
E' -> - T E'
E' -> ε
T  -> F T'
T' -> * F T'
T' -> / F T'
T' -> ε
F -> ( E )
F -> literal
"""

LITERAL = '1234567890'
input_string = []
token = None
index = 0
debug = True


def eat(str):
    """Verifica si el token que está por leerse es el esperado,
    si es así avanza, si no, lanza excepción."""
    global token, input_string, index
    if token in str:
        if debug: print(token)
        token = input_string[index]
        index = index + 1
        return True
    else:
        return False


def reset(idx):
    if debug: print("reset to {}".format(str(idx)))
    global index
    index = idx
    return True


def parse(str):
    """Verifica que un string cumple con la gramática que comienza en A().
    """
    global input_string, token, index
    input_string = list(str + 'E')
    token = input_string[index]
    index = index + 1
    E()
    if len(input_string)==index and token == 'E':
        print('Success')
    else:
        print('Error')


# Reglas de la gramática
def E():
    if debug: print("E")
    return T() and Ep()


def Ep():
    global index
    backup = index
    if debug: print("Ep")
    return ((reset(backup) and eat('+') and T() and Ep()) or
            (reset(backup) and eat('-') and T() and Ep()) or
            (reset(backup) and epsilon()))


def T():
    if debug: print("T")
    return F() and Tp()


def Tp():
    global index
    backup = index
    if debug: print("Tp")
    return ((reset(backup) and eat('*') and F() and Tp()) or
            (reset(backup) and eat('/') and F() and Tp()) or
            (reset(backup) and epsilon()))


def F():
    if debug: print("F")
    return eat(LITERAL) or (eat('(') and E() and eat(')'))


def epsilon():
    if debug: print("epsilon")
    return True


if __name__ == '__main__':
    parse('(5+9*4)')