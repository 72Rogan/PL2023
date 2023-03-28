import ply.lex as lex
import re

print("Insira o caminho para o ficheiro .p ao qual fazer a análise léxica.")
fich = input(">> ")

f = open(fich)
texto = ""
for line in f.readlines():
    texto += line
f.close()

# List of token names.   This is always required
tokens = (
    'COMENTARIO',
    'MULTICOMENTARIO',
    'VAR',
    'TYPE',
    'FUNCAO',
    'PROGRAM',
    'LOOP',
    'CONDICAO',
    'OPERACAO',
    'SEMICOLON',
    'EQUALS',    
    'LISTA',
    'ARRAY',
    'PARENTINIT',
    'PARENTEND'
)

# Regular expression rules for simple tokens
t_COMENTARIO = r"(\/\/.*)"
t_MULTICOMENTARIO = r"(\/\*(.*|\n)+\*\/)"
t_VAR = r"\w+(\w+)?"
t_TYPE = r"(int|double|float|char|string)"
t_FUNCAO = r"function\s*\w+\((\s*\w+\s*,)*\s*\w+\s*\)"
t_PROGRAM = r"program\s*\w+"
t_LOOP = r"(while|for)"
t_CONDICAO = r"if|else"
t_OPERACAO = r"\+|\-|\*|\/"
t_SEMICOLON = r";"
t_EQUALS = r"="
t_LISTA = r"\{.*\}"
t_ARRAY = r"\[.*\]"

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
        
# Construção do lexer
lexer = lex.lex()
lexer.input(texto)
while True:
    tok = lexer.token()
    if not tok: # Não é um token
        break
    print(tok)