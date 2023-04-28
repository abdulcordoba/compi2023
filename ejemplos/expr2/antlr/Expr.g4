grammar Expr;           
prog:   (expr NEWLINE)* ;
expr:   expr op=MULT expr  # mult
    |   expr op=DIV expr   # div
    |   expr op=ADD expr   # add
    |   expr op=SUB expr   # sub
    |   INT             # int
    |   LPAR expr RPAR    # parens
    ;

MULT: '*';
DIV: '/';
ADD: '+';
SUB: '-';
NEWLINE : [\r\n]+ -> skip;
INT     : [0-9]+ ;

LPAR : '(';
RPAR : ')';