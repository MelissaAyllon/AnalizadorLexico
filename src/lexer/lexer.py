import ply.lex as lex

from lexer.reserved import reserved
from lexer.logger import create_log_file

tokens = ['NEWLINE', 'ID', # Identifier
          'NULLABLE', 'LPAREN', 'RPAREN', 'RBRACKET', 'LBRACKET', 'LBRACE', 'RBRACE', 'LT', 'GT', 'ASSIGN', 'SEMI', 'COMA', 'DOT', 'COLON',  # Literals
          'CUSTOM_TYPE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'AND', 'OR', 'NOT', 'EQ', 'NEQ', # Operators
            'INT', 'DOUBLE', 'STRING', 'BOOL', # Data types
         ] + list(reserved.values()) 

'''
Reserved words are defined in reserved.py
and imported here.

Functions and literals are defined here for tokenization.
The lexer will recognize these tokens in the input data.
'''

# CONTRIBUTION: MELISSA AYLLON
t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_NULLABLE(t):
    r'\?'
    t.type = 'NULLABLE'
    return t

def t_LPAREN(t):
    r'\('
    t.type = 'LPAREN'
    return t

def t_RPAREN(t):
    r'\)'
    t.type = 'RPAREN'
    return t

def t_LBRACKET(t):
    r'\['
    t.type = 'LBRACKET'
    return t

def t_RBRACKET(t):
    r'\]'
    t.type = 'RBRACKET'
    return t

lexer_errors = []  # List for storing lexical errors
# Lexical errors
def t_error(t):
    error_message = f"Caracter ilegal '{t.value[0]}' en línea {t.lexer.lineno}, posición {t.lexpos}"
    lexer_errors.append(error_message)
    print(error_message)
    t.lexer.skip(1)
    return error_message





# CONTRIBUTION: NOELIA PASACA

def t_CUSTOM_TYPE(t):
    r'\b([A-Z][a-zA-Z0-9]*)\b'  # Identifiers that start with an uppercase letter
    t.type = 'CUSTOM_TYPE'
    return t

# Operators
def t_PLUS(t):
    r'\+'
    t.type = 'PLUS'
    return t

def t_MINUS(t):
    r'-'
    t.type = 'MINUS'
    return t

# CONTRIBUTION: CARLOS SALAZAR
def t_COMMENT_SINGLE_LINE(t):
    r'//.*'
    # Single-line comment, ignore it
    pass

def t_COMMENT_MULTI_LINE(t):
    r'/\*(.|\n)*?\*/'
    # Multi-line comment, ignore it
    t.lexer.lineno += t.value.count('\n')
    pass

# CONTRIBUTION: NOELIA PASACA
def t_EQ(t):
    r'=='
    t.type = 'EQ'
    return t    

def t_NEQ(t):
    r'!='
    t.type = 'NEQ'
    return t

def t_TIMES(t):
    r'\*'
    t.type = 'TIMES'
    return t

def t_DIVIDE(t):
    r'/'
    t.type = 'DIVIDE'
    return t

def t_MOD(t):
    r'%'
    t.type = 'MOD'
    return t

def t_AND(t):
    r'&&'
    t.type = 'AND'
    return t

def t_OR(t):
    r'\|\|'
    t.type = 'OR'
    return t

def t_NOT(t):
    r'!'
    t.type = 'NOT'
    return t



# CONTRIBUTION: CARLOS SALAZAR

def t_DOUBLE(t):
    r'\b\d+\.\d+\b'  # Matches floating-point numbers
    t.value = float(t.value)  # Convert to float
    t.type = 'DOUBLE'
    return t


def t_INT(t):
    r'\b\d+\b'  # Matches integers
    t.value = int(t.value)  # Convert to integer
    t.type = 'INT'
    return t

def t_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'  # Matches double-quoted strings
    t.value = t.value[1:-1]  # Remove the quotes
    t.type = 'STRING'
    return t

def t_BOOL(t):
    r'\b(true|false)\b'  # Matches boolean literals
    t.value = (t.value == 'true')  # Convert to boolean
    t.type = 'BOOL'
    return t

def t_SEMI(t):
    r';'
    t.type = 'SEMI'
    return t

def t_ASSIGN(t):
    r'='
    t.type = 'ASSIGN'
    return t

def t_COMA(t):
    r','
    t.type = 'COMA'
    return t

def t_LT(t):
    r'<'
    t.type = 'LT'
    return t

def t_GT(t):
    r'>'
    t.type = 'GT'
    return t

def t_LBRACE(t):
    r'\{'
    t.type = 'LBRACE'
    return t

def t_RBRACE(t):
    r'\}'
    t.type = 'RBRACE'
    return t

# CONTRIBUTION: NOELIA PASACA
def t_DOT(t):
    r'\.'
    t.type = 'DOT'
    return t

# CONTRIBUTION: NOELIA PASACA
def t_COLON(t):
    r':'
    t.type = 'COLON'
    return t

# Create the global lexer object: so that it recognizes the parser
lexer = lex.lex()
lexer.lineno = 1 
#--- Function to get tokens from input data
def get_tokens(data):
    # Build the lexer
    global lexer
    lexer.lineno = 1  # Reset counter for each analysis
    
    # Clean up previous errors
    lexer_errors.clear()
    
    # Give the lexer some input
    lexer.input(data)

    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        tokens_list.append(str(tok))  # Store the token as string
    return tokens_list

'''
# Example usage of the lexer
Testing the lexer with a sample input
and writing the tokens to a log file.
'''

# Function to analyze a specific line
def analyze_line(line_content, line_number):
    """Analiza una línea específica de código"""
    global lexer
    lexer.lineno = line_number
    lexer.input(line_content)
    
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    
    return tokens

def read_dart_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: file not found {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return ""

def process_dart_file(file_path):
    """Process a Dart file and return the tokens found"""
    data = read_dart_file(file_path)
    if not data:
        return []
    return get_tokens(data)

def main():
    dart_files = [
        "tests/dart_examples/algoritmo_noelia.dart",
        "tests/dart_examples/algoritmo_melissa.dart",
        "tests/dart_examples/algoritmo_carlos.dart"
    ]

    for file_path in dart_files:
        print(f"\nProcesando archivo: {file_path}")
        tokens_list = process_dart_file(file_path)
        if tokens_list:
            create_log_file(tokens_list, file_path)
            print(f"Tokens encontrados: {len(tokens_list)}")
        else:
            print(f"No se pudieron procesar tokens para {file_path}")

if __name__ == "__main__":
    main()