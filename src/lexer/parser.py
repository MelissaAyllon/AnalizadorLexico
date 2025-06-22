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
                  | NOT expression
                  | expression EQ expression
                  | expression NEQ expression'''
    if len(p) == 2:  # Base case: just a boolean literal
        p[0] = p[1] == 'true'  # 'TRUE' becomes True, 'FALSE' becomes False
    elif p[2] == '&&':  # Logical AND
        p[0] = p[1] and p[3]
    elif p[2] == '||':  # Logical OR
        p[0] = p[1] or p[3]
    elif p[1] == '!':  # Logical NOT
        p[0] = not p[2]
    elif p[2] == '==':  # Equality check
        p[0] = p[1] == p[3] # True if equal, False otherwise
    elif p[2] == '!=':  # Inequality check
        p[0] = p[1] != p[3]  # True if not equal, False otherwise

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

# CONTRIBUCION: CARLOS SALAZAR

# Rule for print statement
def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMI'''
    print(f"Imprimiendo: {p[3]}")
    
# Rule for input statement
def p_statement_input(p):
    '''expression : STDIN DOT READLINESYNC LPAREN RPAREN'''
    p[0] = input("Entrada del usuario: ")
    

def p_statement_List(p):
    '''statement : LIST LT type GT ID ASSIGN LBRACKET RBRACKET SEMI
                 | LIST LT type GT ID ASSIGN LBRACKET group RBRACKET SEMI
                 | LIST ID ASSIGN LBRACKET group RBRACKET SEMI'''
    if len(p) == 10:  # Empty list
        print(f"Declarando lista vacía '{p[5]}'")
    elif len(p) > 10:  # List with elements
        print(f"Declarando lista '{p[5]}' con elementos {p[8]}")
        
def p_statement_type(p):
    '''type : INT
            | STRING
            | BOOL
            | DOUBLE
            | CUSTOM_TYPE
            | VAR'''
def p_List_expression(p):
    '''group : expression COMA group
            | expression'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]
    

# Rule for while statement    
def p_statement_while(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACE statement RBRACE'''
    print("Bucle 'while' encontrado")


# Rule for for class
    
def p_statement_class(p):
    '''statement : CLASS ID LBRACE class_body RBRACE'''
    print(f"Definiendo clase '{p[2]}' con cuerpo {p[4]}")

# Rule for class body with single or multiple statements
                  
def p_class_body_single(p):
    'class_body : statement'
    p[0] = [p[1]]  

def p_class_body_multiple(p):
    'class_body : statement class_body'
    p[0] = [p[1]] + p[2]  
    
def p_statement_function_with_params(p):
    'statement : VOID ID LPAREN param_list RPAREN LBRACE statement RBRACE'
    print(f"Definiendo función '{p[2]}' con parámetros {p[4]} y cuerpo: {p[6]}")

def p_statement_function_no_params(p):
    'statement : VOID ID LPAREN RPAREN LBRACE statement RBRACE'
    print(f"Definiendo función '{p[2]}' sin parámetros, con cuerpo: {p[6]}")

def p_param_list_multiple(p):
    'param_list : param COMA param_list'
    p[0] = [p[1]] + p[3]

def p_param_list_single(p):
    'param_list : param'
    p[0] = [p[1]]

def p_param(p):
    'param : type ID'
    p[0] = (p[1], p[2])

parser = yacc.yacc()

while True:
   try:
       s = input('dart > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)