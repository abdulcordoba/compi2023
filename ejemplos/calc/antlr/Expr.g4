grammar Expr;

prog:   (expr NEWLINE)* ;
expr:   expr op=MULT expr   # mult
    |   expr op=DIV expr   # div
    |   expr op=ADD expr  # add
    |   expr op=SUB expr   # sub
    |   INT             # int
    |   '(' expr ')'    # parens
    ;

MULT: '*';
DIV: '/';
ADD: '+';
SUB: '-';
NEWLINE : [\r\n]+ ;
INT     : [0-9]+ ;