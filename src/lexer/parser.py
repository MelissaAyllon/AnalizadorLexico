import ply.yacc as yacc
from lexer import tokens

# --- Grammar Rules ---
precedence = (
    ('left', 'OR', 'AND'),    # 'OR' and 'AND' are left-associative
    ('left', 'PLUS', 'MINUS'),  # 'PLUS' and 'MINUS' are left-associative
    ('left', 'TIMES', 'DIVIDE'),  # 'TIMES' and 'DIVIDE' are left-associative
    ('right', 'NOT'),          # 'NOT' is right-associative
)


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

# Regla para el condicional if
def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE
                 | IF LPAREN expression RPAREN LBRACE statement RBRACE ELSE LBRACE statement RBRACE'''
    print("Condicional 'if' encontrado")
    
# Rule for numeric expressions
def p_expression_number(p):
    '''expression : INT
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if len(p) == 2:  # Base case: just a number
        p[0] = p[1]
    else:  # If it's an operation, perform it
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

# Rule for string expressions (concatenation)
def p_expression_string(p):
    '''expression : STRING'''
    if len(p) == 2:  # Base case: just a string
        p[0] = p[1]

# Rule for boolean expressions
def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE
                  | expression AND expression
                  | expression OR expression
                  | NOT expression'''
    if len(p) == 2:  # Base case: just a boolean literal
        p[0] = p[1] == 'true'  # 'TRUE' becomes True, 'FALSE' becomes False
    elif p[2] == '&&':  # Logical AND
        p[0] = p[1] and p[3]
    elif p[2] == '||':  # Logical OR
        p[0] = p[1] or p[3]
    elif p[1] == '!':  # Logical NOT
        p[0] = not p[2]

# Rule for grouping expressions (use parentheses to group expressions)
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

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