import ply.yacc as yacc
from lexer.lexer import tokens
from lexer.lexer import lexer
from lexer.logger import process_test_directory_parser, create_parser_log_file
import os

tabla_simbolos = {
    'var': {},
    "tipos": {
        "str_functions": ["toUpperCase", "toLowerCase", "substring", "length"],
    },
    "clases": {}
}

semantic_errors = []  # List for storing semantic errors

# --- Grammar Rules ---
precedence = (
    ('left', 'OR', 'AND'),    # 'OR' and 'AND' are left-associative
    ('left', 'PLUS', 'MINUS'),  # 'PLUS' and 'MINUS' are left-associative
    ('left', 'TIMES', 'DIVIDE'),  # 'TIMES' and 'DIVIDE' are left-associative
    ('right', 'NOT'),          # 'NOT' is right-associative
)

# ===== SEMANTIC RULES PER MEMBER =====
# CARLOS SALAZAR - Semantic rules for data structures
def validate_list_declaration(var_name, elements):
    """Regla semántica 1 de Carlos: Validar que los elementos de una lista sean del mismo tipo"""
    if elements and len(elements) > 1:
        first_type = type(elements[0])
        for i, element in enumerate(elements[1:], 1):
            if type(element) != first_type:
                error_msg = f"Error semántico: Lista '{var_name}' debe contener elementos del mismo tipo. Elemento {i} es {type(element).__name__}, se esperaba {first_type.__name__}"
                semantic_errors.append(error_msg)
                print(error_msg)
                return False
    return True

def validate_map_key_types(var_name, entries):
    """Regla semántica 2 de Carlos: Validar que las claves del map sean del mismo tipo"""
    if entries and len(entries) > 1:
        first_key_type = type(entries[0][0])
        for i, (key, value) in enumerate(entries[1:], 1):
            if type(key) != first_key_type:
                error_msg = f"Error semántico: Map '{var_name}' debe tener claves del mismo tipo. Clave {i} es {type(key).__name__}, se esperaba {first_key_type.__name__}"
                semantic_errors.append(error_msg)
                print(error_msg)
                return False
    return True

# MELISSA AYLLON - Semantic rules for control structures
def validate_loop_condition(condition, loop_type):
    """Regla semántica 1 de Melissa: Validar que las condiciones de bucle sean booleanas"""
    if not isinstance(condition, bool):
        error_msg = f"Error semántico: La condición del bucle {loop_type} debe ser booleana, se recibió {type(condition).__name__}"
        semantic_errors.append(error_msg)
        print(error_msg)
        return False
    return True

def validate_if_condition(condition):
    """Regla semántica 2 de Melissa: Validar que las condiciones de if sean booleanas"""
    if not isinstance(condition, bool):
        error_msg = f"Error semántico: La condición del if debe ser booleana, se recibió {type(condition).__name__}"
        semantic_errors.append(error_msg)
        print(error_msg)
        return False
    return True

# NOELIA PASACA - Semantic rules for functions and validations
def validate_function_return_type(func_name, expected_type, actual_value):
    """Regla semántica 1 de Noelia: Validar que las funciones retornen el tipo esperado"""
    if expected_type == 'double' and not isinstance(actual_value, (int, float)):
        error_msg = f"Error semántico: Función '{func_name}' debe retornar double, se recibió {type(actual_value).__name__}"
        semantic_errors.append(error_msg)
        print(error_msg)
        return False
    elif expected_type == 'bool' and not isinstance(actual_value, bool):
        error_msg = f"Error semántico: Función '{func_name}' debe retornar bool, se recibió {type(actual_value).__name__}"
        semantic_errors.append(error_msg)
        print(error_msg)
        return False
    return True

def validate_parameter_types(func_name, param_name, expected_type, actual_value):
    """Regla semántica 2 de Noelia: Validar tipos de parámetros en funciones"""
    if expected_type == 'int' and not isinstance(actual_value, int):
        error_msg = f"Error semántico: Parámetro '{param_name}' en función '{func_name}' debe ser int, se recibió {type(actual_value).__name__}"
        semantic_errors.append(error_msg)
        print(error_msg)
        return False
    elif expected_type == 'double' and not isinstance(actual_value, (int, float)):
        error_msg = f"Error semántico: Parámetro '{param_name}' en función '{func_name}' debe ser double, se recibió {type(actual_value).__name__}"
        semantic_errors.append(error_msg)
        print(error_msg)
        return False
    return True

# Contributed by: MELISSA AYLLON
def p_statement_class(p):
    '''statement : CLASS ID LBRACE class_body RBRACE'''
    nombre_clase = p[2]
    if nombre_clase not in tabla_simbolos['clases']:
        tabla_simbolos['clases'][nombre_clase] = {'atributos': [], 'metodos': []}
    print(tabla_simbolos['clases'])
    print(f"Definiendo clase '{nombre_clase}' con cuerpo {p[4]}")

def p_type(p):
    '''type : INT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | DOUBLE_TYPE
            | ID
            '''
    if p.slice[1].type == 'ID':
        if p[1] not in tabla_simbolos['clases']:
            raise TypeError(f"El tipo personalizado '{p[1]}' no está definido como clase.")
    p[0] = p[1]

# Variable Assignment (Generalized)
def p_statement_assign_simple(p):
    '''statement : type ID ASSIGN expression SEMI
                 | VAR ID ASSIGN expression SEMI
                 | FINAL ID ASSIGN expression SEMI
    '''
    tipo_variable = p[1]
    nombre_variable = p[2]
    valor = p[4]

    valid_assignment = True

    if tipo_variable == 'int':
        try:
            if isinstance(valor, str):
                valor = valor.strip('"')
            valor = int(valor)
        except ValueError:
            error_message = f"Error semántico: la variable '{nombre_variable}' debe ser int, pero se recibió '{valor}'"
            print(error_message)
            semantic_errors.append(error_message)  # Save semantic error
            valid_assignment = False


    elif tipo_variable == 'double':
        try:
            if isinstance(valor, str):
                valor = valor.strip('"')
            valor = float(valor)
        except ValueError:
            error_message = f"Error semántico: la variable '{nombre_variable}' debe ser double, pero se recibió '{valor}'"
            print(error_message)
            semantic_errors.append(error_message)  # Save semantic error
            valid_assignment = False
        
    elif tipo_variable == 'bool':
        if isinstance(valor, str):
            valor_lower = valor.lower().strip('"')
            if valor_lower == 'true':
                valor = True
            elif valor_lower == 'false':
                valor = False
            else:
                error_message = f"Error semántico: la variable '{nombre_variable}' debe ser bool ('true' o 'false'), pero se recibió '{valor}'"
                print(error_message)
                semantic_errors.append(error_message)  # Save semantic error
                valid_assignment = False
        elif not isinstance(valor, bool):
            error_message = f"Error semántico: la variable '{nombre_variable}' debe ser bool, pero se recibió un tipo {type(valor).__name__}"
            print(error_message)
            semantic_errors.append(error_message)  # Save semantic error
            valid_assignment = False

    elif tipo_variable == 'String':
        if not isinstance(valor, str):
            error_message = f"Error semántico: la variable '{nombre_variable}' debe ser String, pero se recibió un tipo {type(valor).__name__}"
            print(error_message)
            semantic_errors.append(error_message)  # Save semantic error
            valid_assignment = False
        else:
            valor = valor.strip('"')  # Optional: clear quotes

    # If the type is 'var', we let the type be inferred without validation.

    if valid_assignment:
        if nombre_variable in tabla_simbolos['var']:
            print(f"Advertencia: La variable '{nombre_variable}' ya existe, se actualizará su valor.")
        tabla_simbolos['var'][nombre_variable] = {'type': tipo_variable, 'value': valor}
        print(f"Variable '{nombre_variable}' declarada con tipo '{tipo_variable}' y valor '{valor}'")
    else:
        print(f"No se declaró la variable '{nombre_variable}' por error de tipo.")



def p_statement_assign_new_instance(p):
    '''statement : ID ID ASSIGN NEW ID LPAREN RPAREN SEMI'''
    tipo_variable = p[1]
    nombre_variable = p[2]
    clase_nueva = p[5]
    # To instantiate a new object (no value is evaluated yet, just that it is an instance)
    if nombre_variable in tabla_simbolos['var']:
        print(f"Advertencia: La variable '{nombre_variable}' ya existe, se actualizará su valor.")
    tabla_simbolos['var'][nombre_variable] = {'type': tipo_variable, 'value': f'new {clase_nueva}()'}
    print(f"Variable '{nombre_variable}' declarada como nueva instancia de '{clase_nueva}'")


    # Check if the variable already exists
    if nombre_variable in tabla_simbolos['var']:
        raise NameError(f"La variable '{nombre_variable}' ya ha sido declarada.")

    # Type checking for reserved types
    if tipo_variable == 'var':
        tipo_inferido = type(valor).__name__
        tabla_simbolos['var'][nombre_variable] = {'type': tipo_inferido, 'value': valor}
    elif tipo_variable == 'final':
        tabla_simbolos['var'][nombre_variable] = {'type': 'final', 'value': valor}
    elif tipo_variable == 'String' and not isinstance(valor, str):
        raise TypeError(f"Se esperaba String para '{nombre_variable}', pero se recibió {type(valor).__name__}")
    elif tipo_variable == 'int' and not isinstance(valor, int):
        raise TypeError(f"Se esperaba int para '{nombre_variable}', pero se recibió {type(valor).__name__}")
    elif tipo_variable == 'double' and not isinstance(valor, float):
        raise TypeError(f"Se esperaba double para '{nombre_variable}', pero se recibió {type(valor).__name__}")
    elif tipo_variable == 'bool' and not isinstance(valor, bool):
        raise TypeError(f"Se esperaba bool para '{nombre_variable}', pero se recibió {type(valor).__name__}")
    # Checking for custom types (classes)
    elif tipo_variable in tabla_simbolos['clases']:
        # Logic to verify that the value is a valid instance
        tabla_simbolos['var'][nombre_variable] = {'type': tipo_variable, 'value': valor}
    else:
        tabla_simbolos['var'][nombre_variable] = {'type': tipo_variable, 'value': valor}

    print(f"Variable '{nombre_variable}' declarada con tipo '{tipo_variable}' y valor '{valor}'")
    print(f"Tabla de símbolos actualizada: {tabla_simbolos['var']}")

# Rule for the if conditional
def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE
                 | IF LPAREN expression RPAREN LBRACE statement RBRACE ELSE LBRACE statement RBRACE'''
    if len(p) == 8:  # if without else
        condition = p[3]
        then_body = p[6]
        print(f"Condicional 'if' encontrado con condición: {condition}")
        print(f"Cuerpo del if: {then_body}")
        # Apply Melissa's semantic rule: validate boolean condition
        validate_if_condition(condition)
    else:  # if with else
        condition = p[3]
        then_body = p[6]
        else_body = p[10]
        print(f"Condicional 'if-else' encontrado con condición: {condition}")
        print(f"Cuerpo del if: {then_body}")
        print(f"Cuerpo del else: {else_body}")
        # Apply Melissa's semantic rule: validate boolean condition
        validate_if_condition(condition)

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
    nombre = p[1]
    if nombre in tabla_simbolos['var']:
        p[0] = tabla_simbolos['var'][nombre]['value']
    else:
        print(f"Error semántico: variable '{nombre}' no declarada")
        p[0] = None

def p_expression_attribute(p):
    'expression : expression DOT ID'
    print(f"Accediendo al atributo '{p[3]}' de {p[1]}")

parser_errors = []  # List to store syntactical errors
current_line = 1
def p_error(p):
    global current_line
    
    if p:
        # Use the current line of the problematic token
        error_line = p.lineno if p.lineno else current_line
        
        print("DEBUG token p:", p)
        print("p.value:", repr(p.value))  # use repr to view special characters
        print("p.type:", p.type)
        print("p.lineno:", p.lineno)
        print("p.lexpos:", p.lexpos)
        print("current_value:", current_line)
        
        # More detailed analysis of the error
        if p.type == 'NEWLINE':
            # If the error is in NEWLINE
            error_message = f"Error de sintaxis en línea {current_line}: Declaración incompleta o mal formada"
            current_line = 1
        elif p.type == 'SEMI':
            error_message = f"Error de sintaxis en línea {current_line}: Falta punto y coma (;) después de '{p.value}'"
            current_line = 1
        elif p.type == 'RBRACE':
            error_message = f"Error de sintaxis en línea {current_line}: Falta llave de cierre (}}) después de '{p.value}'"
        elif p.type == 'RPAREN':
            error_message = f"Error de sintaxis en línea {current_line}: Falta paréntesis de cierre ()) después de '{p.value}'"
        elif p.type == 'RBRACKET':
            error_message = f"Error de sintaxis en línea {current_line}: Falta corchete de cierre (]) después de '{p.value}'"
        elif p.type == 'ID':
            error_message = f"Error de sintaxis en línea {current_line}: Token inesperado '{p.value}'. Posible declaración de tipo faltante"
        else:
            error_message = f"Error de sintaxis en línea {current_line}: Token inesperado '{p.value}' de tipo '{p.type}'"
        current_line = 1
        print(f"Capturando error sintáctico: {error_message}")
        parser_errors.append(error_message)
    else:
        error_message = "Error de sintaxis: Fin inesperado de entrada. Verifique que todas las declaraciones terminen con punto y coma (;) y que todas las llaves estén cerradas"
        print(f"Capturando error sintáctico: {error_message}")
        parser_errors.append(error_message)
        current_line = 1

    # Stop the analysis immediately
    raise SyntaxError(error_message)


def p_statement_newline(p):
    '''statement : NEWLINE'''
    global current_line
    current_line += 1
    pass  # We just ignore line breaks, they don't cause errors

''' 
    Main program to test the parser
    EG. dart > var x = 10;
    EG. dart > var name = "Dart";
'''

# CONTRIBUTION: CARLOS SALAZAR

# Rule for print statement
def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMI'''
    if not isinstance(p[3], (int, float, str, bool)):
        print(f"Advertencia: Se está intentando imprimir un tipo no básico: {type(p[3]).__name__}")
    print(f"Imprimiendo: {p[3]}")
    
# Rule for input statement
def p_statement_input(p):
    '''expression : STDIN DOT READLINESYNC LPAREN RPAREN'''
    entrada = input("Entrada del usuario: ")
    p[0] = entrada  # Always returns string, could be extended with cast
    print(f"Entrada registrada: '{entrada}' (tipo: {type(entrada).__name__})")

    

def p_statement_List(p):
    '''statement : LIST LT type GT ID ASSIGN LBRACKET RBRACKET SEMI
                 | LIST LT type GT ID ASSIGN LBRACKET group RBRACKET SEMI
                 | LIST ID ASSIGN LBRACKET group RBRACKET SEMI'''
    
    if len(p) == 10:  # Empty list
        nombre_var = p[5] if p.slice[1].type == 'LIST' else p[2]
        tabla_simbolos['var'][nombre_var] = {'type': 'list', 'value': []}
        print(f"Declarando lista vacía '{nombre_var}'")
    
    else:  # List with elements
        nombre_var = p[5] if p.slice[1].type == 'LIST' else p[2]
        elementos = p[8] if p.slice[1].type == 'LIST' else p[6]
        
        # Apply Carlos's semantic rule: validate element types
        if validate_list_declaration(nombre_var, elementos):
            tabla_simbolos['var'][nombre_var] = {'type': 'list', 'value': elementos}
            print(f"Declarando lista '{nombre_var}' con elementos {elementos}")
        else:
            print(f"No se declaró la lista '{nombre_var}' por error semántico")

        
def p_List_expression(p):
    '''group : expression COMA group
            | expression'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

# Rule for while statement    
def p_statement_while(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACE statement RBRACE'''
    condition = p[3]
    body = p[6]
    print(f"Bucle 'while' encontrado con condición: {condition}")
    print(f"Cuerpo del while: {body}")
    # Apply Melissa's semantic rule: validate boolean condition
    validate_loop_condition(condition, "while")
    # Semantic analysis: check for possible infinite loop
    if condition == True:
        print("Advertencia: Condición siempre verdadera - posible bucle infinito")

# CONTRIBUTION: NOELIA PASACA

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
        nombre_var = p[7]
        tabla_simbolos['var'][nombre_var] = {'type': 'map', 'value': {}}
        print(f"Declarando mapa vacío '{nombre_var}' de tipo {p[2]}<{p[3]}, {p[5]}>")
    else:  # Map with entries
        nombre_var = p[7]
        entradas = p[10]
        
        # Apply Carlos's semantic rule: validate key types
        if validate_map_key_types(nombre_var, entradas):
            tabla_simbolos['var'][nombre_var] = {'type': 'map', 'value': dict(entradas)}
            print(f"Declarando mapa '{nombre_var}' de tipo {p[2]}<{p[3]}, {p[5]}> con entradas {entradas}")
        else:
            print(f"No se declaró el mapa '{nombre_var}' por error semántico")

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
                  
def p_class_body_empty(p):
    'class_body : '
    p[0] = []

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
    
def p_program(p):
    '''program : statements'''
    p[0] = p[1]
    
def p_statement_empty(p):
    '''statement : '''
    pass

def p_statements_multiple(p):
    '''statements : statements statement'''
    if p[2] is not None:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]

def p_statements_single(p):
    '''statements : statement'''
    if p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

parser = yacc.yacc(start='program')

def parse_code(code):
    """Función para parsear código con mejor manejo de errores"""
    global current_line

    
    # Reset counters
    current_line = 1
    lexer.lineno = 1
    lexer.lexpos = 0
    parser_errors.clear()
    semantic_errors.clear()
    # Reset symbol table
    tabla_simbolos['var'].clear()
    tabla_simbolos['clases'].clear()

    parser.restart()
    
    try:
        # Clean up trailing empty lines from your code
        code = code.strip()
        if not code:
            print("No hay código para analizar")
            return None
        if not code.endswith('\n'):
            code += '\n'
        result = parser.parse(code, lexer=lexer)
        return result
    except SyntaxError as e:
        print(f"Análisis detenido por error sintáctico: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado durante el análisis: {e}")
        return None

def main():
    """Función principal que procesa archivos de prueba y crea logs"""
    print("=== Analizador Sintáctico para Dart ===")
    
    # Process all test files
    results = process_test_directory_parser(parser)
    
    # Reset counters
    current_line = 1
    lexer.lineno = 1
    parser_errors.clear()
    semantic_errors.clear()
    
    if results:
        # Create log file with the results
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
        print("Escribe tu código Dart. Termina con Ctrl+D (EOF) para analizar:")

        code = ""
        try:
            while True:
                line = input()
                code += line + "\n"
        except EOFError:
            pass
    
        # Using the new parsing function
        result = parse_code(code)
        
        
        if result:
            print("Análisis completado exitosamente")
            print("Tabla de símbolos:", tabla_simbolos)
             # Reset counters
            current_line = 1
            lexer.lineno = 1
            parser_errors.clear()
            semantic_errors.clear()
        
        # Show errors found
        if parser_errors:
            print("\nErrores sintácticos:")
            for error in parser_errors:
                print(f"  - {error}")
            # Reset counters
            current_line = 1
            lexer.lineno = 1
            parser_errors.clear()
            semantic_errors.clear()
        else:
            print("\nNo hay errores sintácticos.")
            current_line = 1

            
        if semantic_errors:
            print("\nErrores semánticos:")
            for error in semantic_errors:
                print(f"  - {error}")
            #  reset counters
            current_line = 1
            lexer.lineno = 1
            parser_errors.clear()
            semantic_errors.clear()

        else:
            print("\nNo hay errores semánticos.")
            # Reset counters
            current_line = 1
            lexer.lineno = 1
            parser_errors.clear()
            semantic_errors.clear()

    else:
        print("Opción no válida. Saliendo...")
        exit(1)
