import ply.lex as lex
from reserved import reserved

tokens = ['ID'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

print("Tokens:", tokens)

# Define a rule for ignored characters (whitespace, newlines)
t_ignore = ' \t\n'

# Test it out
data = '''
function
'''
# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)