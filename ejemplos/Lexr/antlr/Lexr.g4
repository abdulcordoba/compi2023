grammar Lexr;

@members {
count = 0
holamundo = "Hola mundo"
}

secuencia_de_cosas : cosa+;

cosa :  
    MULT
    |   DIV
    |   ADD
    |   SUB
    |   ID
    |   INT {self.count = self.count + 1}
    |   FLOAT {self.count = self.count + 1}
    ;

MULT: '*';
DIV: '/';
ADD: '+';
SUB: '-';
INT : DIGIT+ ; // references the DIGIT helper rule
fragment DIGIT : [0-9] ; // not a token by itself
FLOAT : DIGIT+ '.' DIGIT+;
ID : [a-z]+;

WS : [ \r\t\n]+ -> skip ;


