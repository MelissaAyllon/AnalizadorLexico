import ply.lex as lex
from reserved import reserved
from logger import create_log_file

tokens = ['NEWLINE', 'ID', # Identifier
          'NULLABLE', 'LPAREN', 'RPAREN', 'RBRACKET', 'LBRACKET', 'LBRACE', 'RBRACE', 'LT', 'GT', 'ASSIGN', 'SEMI', 'COMA',  # Literals
          'CUSTOM_TYPE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'AND', 'OR', 'NOT', # Operators
         ] + list(reserved.values()) 

'''
Reserved words are defined in reserved.py
and imported here.

Functions and literals are defined here for tokenization.
The lexer will recognize these tokens in the input data.
'''

# CONTRIBUCION: MELISSA AYLLON
t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.type = 'NEWLINE'
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

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.type = 'ILLEGAL'
    t.lexer.skip(1)
    return "'%s'" % t.value[0] + " (illegal character)"

# CONTRIBUCION: NOELIA PASACA

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

# CONTRIBUCION: CARLOS SALAZAR
def t_COMMENT_SINGLE_LINE(t):
    r'//.*'
    # Single-line comment, ignore it
    pass

def t_COMMENT_MULTI_LINE(t):
    r'/\*(.|\n)*?\*/'
    # Multi-line comment, ignore it
    t.lexer.lineno += t.value.count('\n')
    pass


# CONTRIBUCION: NOELIA PASACA
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

# CONTRIBUCION: CARLOS SALAZAR

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


#--- Function to get tokens from input data
def get_tokens(data):
    # Build the lexer
    lexer = lex.lex()
    
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

data = '''
function {} [] testFunction()
bool isActive = true;
List<int> numbers = [1, 2, 3, 4];
List<double> numbers = [1.5, 2.3, 3.6, 4.7];
String name = "Carlos Salazar";
// This is a comment
/*This is a 
multi-line comment
*/
CustomType myObject = new CustomType();
double result = 5 + 10 - 3 * 2 / 4 % 1;
'''
# Get tokens from lexico.py
tokens_list = get_tokens(data)

# Create log file and write tokens
create_log_file(tokens_list)