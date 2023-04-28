grammar Small;           

program
    :   (decl|statement)*
    ;

decl
    :   INTEGER ident ';'      #intDecl
    |   BOOL ident_list ';'         #boolDecl
    ;

ident_list
    :   ident ( ',' ident )* 
    ;

ident
    : ID ( '=' expr ) ?
    ;

statement
    :   expr '=' expr ';'                 #assign
    |   PRINT '(' expr ')' ';'              #print
    |   IF '(' expr ')' '{' statement* '}'  #if
    ; 

expr
    :   '!' expr        #not
    |   expr '==' expr  #equal
    |   expr '&&' expr  #and
    |   expr '*' expr   #mult
    |   expr '/' expr   #div
    |   expr '+' expr   #add
    |   expr '-' expr   #sub
    |   INT             #int
    |   STRING          #string
    |   'true'          #true
    |   'false'         #false
    |   ID              #id
    |   '(' expr ')'    #parens
    ;

INT     : [0-9]+ ;
BOOL    : 'bool';
INTEGER : 'int';
PRINT   : 'print';
IF      : 'if';
STRING  : '"' .*? '"' ;
ID      : [a-zA-Z]+ ;

WS : [ \t\n\r]+ -> skip ;