grammar Expr;		

prog:	(expr)* ;

expr:	expr ('*'|'/') expr
    |	expr ('+'|'-') expr
    |	INT
    |	'(' expr ')'
    ;

NEWLINE : [\r\n]+ -> skip;
BLANK   : [ ]+ -> skip;
INT     : [0-9]+ ;



