import ply.yacc as yacc
from lexer import tokens

# --- Parser Rules ---

# Handle numeric expressions
def handle_number(p):
    p[0] = p[1]

# Handle string expressions
def handle_string(p):
    p[0] = p[1]

# --- Grammar Rules ---

# Asignacion de variables (Generalizada)
def p_statement_assign(p):
    '''statement : VAR ID ASSIGN expression SEMI  
                 | FINAL ID ASSIGN expression SEMI
                 | STRING ID ASSIGN expression SEMI
    ''' 
    if p[1] == 'var':
        variable_type = 'var'
    elif p[1] == 'final':
        variable_type = 'final'
    elif p[1] == 'String':
        variable_type = 'String'
    print(f"Declarando variable '{variable_type}' llamada '{p[2]}' con valor {p[4]}")

# Asignacion de expresiones (Generalizada)
def p_expression(p):
    '''expression : INT
                  | STRING'''
    if isinstance(p[1], int):
        handle_number(p)
    elif isinstance(p[1], str):
        handle_string(p)


def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis en la entrada")

''' 
    Main program to test the parser
    EG. dart > var x = 10;
    EG. dart > var name = "Dart";
'''
parser = yacc.yacc()

while True:
   try:
       s = input('dart > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)