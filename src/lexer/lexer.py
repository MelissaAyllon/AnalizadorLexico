import ply.lex as lex
from reserved import reserved
from logger import create_log_file

tokens = ['ID'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


# Define a rule for ignored characters (whitespace, newlines)
t_ignore = ' \t\n'


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


# Test it out
data = '''
function
'''
# Get tokens from lexico.py
tokens_list = get_tokens(data)

# Create log file and write tokens
create_log_file(tokens_list)