from matplotlib.pylab import var
import ply.yacc as yacc
from lexer import tokens
from logger import process_test_directory_parser, create_parser_log_file
import os

tabla_simbolos = {
    'var': {},
    "tipos": {
        "str_functions": ["toUpperCase", "toLowerCase", "substring", "length"],
    }
}


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
                 | STRING_TYPE ID ASSIGN expression SEMI
    ''' 
    if p[1] == 'var':
        variable_type = 'var'
    elif p[1] == 'final':
        variable_type = 'final'
    elif p[1] == 'String':
        variable_type = 'String'
    
    nombre_variable = p[2]
    valor_variable = p[4]

    # --- Semantic type checking ---
    # Infer type of the assigned value
    if isinstance(valor_variable, int):
        value_type = 'int'
    elif isinstance(valor_variable, float):
        value_type = 'double'
    elif isinstance(valor_variable, str):
        value_type = 'String'
    elif isinstance(valor_variable, bool):
        value_type = 'bool'
    else:
        value_type = 'unknown'
    
    
    tabla_simbolos["var"][nombre_variable] = value_type
    print(f"Declarando variable '{variable_type}' llamada '{nombre_variable}' con valor {valor_variable} (tipo detectado: {value_type})")
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

def p_expression_id(p):
    'expression : ID'
    p[0] = p[1]

def p_expression_attribute(p):
    'expression : expression DOT ID'
    print(f"Accediendo al atributo '{p[3]}' de {p[1]}")

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
    '''type : INT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | DOUBLE_TYPE
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

# CONTRIBUCION: NOELIA PASACA

# Rule for for statement (traditional for loop)
def p_statement_for_traditional(p):
    '''statement : FOR LPAREN for_init SEMI expression SEMI for_update RPAREN LBRACE statement RBRACE'''
    print("Bucle 'for' tradicional encontrado")

# Rule for for-in statement (for each loop)
def p_statement_for_in(p):
    '''statement : FOR LPAREN VAR ID IN expression RPAREN LBRACE statement RBRACE'''
    print(f"Bucle 'for-in' encontrado, iterando sobre '{p[4]}' en {p[6]}")

# Rule for for initialization
def p_for_init(p):
    '''for_init : VAR ID ASSIGN expression
                | type ID ASSIGN expression
                | expression'''
    if len(p) == 5:
        print(f"Inicialización de variable '{p[2]}' con valor {p[4]}")
    else:
        p[0] = p[1]

# Rule for for update
def p_for_update(p):
    '''for_update : ID PLUS PLUS
                  | ID MINUS MINUS
                  | ID ASSIGN expression'''
    if p[2] == '++':
        print(f"Incremento de variable '{p[1]}'")
    elif p[2] == '--':
        print(f"Decremento de variable '{p[1]}'")
    else:
        print(f"Actualización de variable '{p[1]}' con valor {p[3]}")

# Rule for Map declaration
def p_statement_map(p):
    '''statement : MAP LT type COMA type GT ID ASSIGN LBRACE map_entries RBRACE SEMI
                 | MAP LT type COMA type GT ID ASSIGN LBRACE RBRACE SEMI'''
    if len(p) == 12:  # Empty map
        print(f"Declarando mapa vacío '{p[7]}' de tipo {p[2]}<{p[3]}, {p[5]}>")
    else:  # Map with entries
        print(f"Declarando mapa '{p[7]}' de tipo {p[2]}<{p[3]}, {p[5]}> con entradas {p[10]}")

# Rule for map entries
def p_map_entries(p):
    '''map_entries : map_entry COMA map_entries
                   | map_entry'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

# Rule for single map entry
def p_map_entry(p):
    '''map_entry : expression COLON expression'''
    p[0] = (p[1], p[3])

# Rule for Set declaration
def p_statement_set(p):
    '''statement : SET LT type GT ID ASSIGN LBRACE set_elements RBRACE SEMI
                 | SET LT type GT ID ASSIGN LBRACE RBRACE SEMI'''
    if len(p) == 11:  # Empty set
        print(f"Declarando conjunto vacío '{p[6]}' de tipo Set<{p[3]}>")
    else:  # Set with elements
        print(f"Declarando conjunto '{p[6]}' de tipo Set<{p[3]}> con elementos {p[9]}")

# Rule for set elements
def p_set_elements(p):
    '''set_elements : expression COMA set_elements
                    | expression'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

# Rule for double expressions
def p_expression_double(p):
    '''expression : DOUBLE
                  | expression PLUS DOUBLE
                  | expression MINUS DOUBLE
                  | expression TIMES DOUBLE
                  | expression DIVIDE DOUBLE
                  | DOUBLE PLUS expression
                  | DOUBLE MINUS expression
                  | DOUBLE TIMES expression
                  | DOUBLE DIVIDE expression'''
    if len(p) == 2:  # Base case: just a double
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

# Rule for class body with single or multiple statements
                  
def p_statement_class(p):
    '''statement : CLASS ID LBRACE class_body RBRACE'''
    print(f"Definiendo clase '{p[2]}' con cuerpo {p[4]}")

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

def main():
    """Función principal que procesa archivos de prueba y crea logs"""
    print("=== Analizador Sintáctico para Dart ===")
    
    # Procesar todos los archivos de prueba
    results = process_test_directory_parser(parser)
    
    if results:
        # Crear archivo de log con los resultados
        test_dir = "tests/dart_examples"
        dart_files = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.endswith('.dart')]
        create_parser_log_file(results, dart_files)
        print(f"Total de resultados procesados: {len(results)}")
    else:
        print("No se encontraron resultados para procesar")

if __name__ == "__main__":
    user_input = input("Para correr el parser de los algoritmos definidos presiona 1 o si quieres inline dart presiona 2 > ")    
    if user_input == '1':
        main()
    elif user_input == '2':
        print("=== Analizador Sintáctico en Línea ===")
        print("Escribe tu código Dart y presiona Enter. Para salir, usa Ctrl+D (EOF).")
        while True:
            try:
                s = input("dart > ")
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            print(result)
    else:
        print("Opción no válida. Saliendo...")
        exit(1)
    