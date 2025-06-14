import ply.lex as lex
from reserved import reserved
from logger import create_log_file

tokens = ['NEWLINE', 'ID', # Identifier
          'NULLABLE', 'LPAREN', 'RPAREN', 'RBRACKET', 'LBRACKET', # Literals
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
hola
    melissa here
'''
# Get tokens from lexico.py
tokens_list = get_tokens(data)

# Create log file and write tokens
create_log_file(tokens_list)