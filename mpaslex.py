#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#------------------------------------------------------------
# lex.py
#
# tokenizer
# ------------------------------------------------------------
import re
import ply.lex as lex
import symtab

reserved = (
# Reserverd words 
#DONE
'ELSE','IF','INT','FLOAT','RETURN','WHILE','FUN','BEGIN','DO','THEN',
'END','PRINT','READ','WRITE','SKIP','BREAK','AND','OR','NOT',
)

reserved_map = { }
for r in reserved:
	reserved_map[r] = r

# List of token names.   
tokens = reserved + (
# Symbols
'PLUS','MINUS','DIVIDE','MULT','LESS','LESSEQUAL','GREATER','GREATEREQUAL',
'DEQUAL','DISTINT','SEMICOLON','COMMA','LPAREN','RPAREN','COLON','LBRACKET',
'RBRACKET','COLONEQUAL',

# Others   
'ID', 
'INUMBER',
'FNUMBER',
#'UMINUS',
##'CHARACTER',
'TEXT',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/(?!\*)'
t_MULT = r'\*'
t_LESSEQUAL = r'<='
t_GREATEREQUAL  = r'>='
t_DEQUAL = r'=='
t_DISTINT = r'!='
t_COLONEQUAL = r':='
t_GREATER = r'>'
t_LESS = r'<'
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_ID(t):
	r'[A-Za-z_][\w]*'
	## problens len 1
	t.type = reserved_map.get(t.value.upper(),'ID')
	if t.type == 'ID':
		symtab.attach_symbol(t)
	return t


#def t_malformed_fnumber(t):
#    r'((0\d+)((\.\d+(e[+-]?\d+)?)|(e[+-]?\d+))) | (\d*(\.\d*(\.)\w*)) | ((\d+)(\.\d*(e[+-]?(?!\d))?)) '
#    print "Linea %d. Malformado numero float '%s'" % (t.lineno, t.value)

def t_FNUMBER(t):
    r'([1-9]\d*|0)(\.\d+(e(\+|-)?\d+)?|e[\+|-]?\d+)'
    return t

def t_malformed_inumber(t):
    r'0\d+(\.\d+(e(\+|-)?\d+)?|e[\+|-]?\d+)?'
    print "Linea %d. Numero mal formado '%s'" % (t.lineno, t.value)

def t_malformed_id(t):
	r'((\\)|(\d+))[A-Za-z]'
	print "Linea %d: Identificador no válido '%s'" % (t.lineno,t.value)

def t_INUMBER(t):
    r'0(?!\d)|([1-9]\d*)'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Linea %d: Numero %s es muy grande!" % (t.lineno,t.value)
        t.value = 0
    return t

def t_TEXT(t):
    r'"[^\n]*?(?<!\\)"'
    temp_str = t.value.replace(r'\\', '')
    m = re.search(r'\\[^n"]', temp_str)
    if m != None:
        print "Linea %d. Caracter de escape no soportado %s en string." % (t.lineno, m.group(0))
    return t

def t_CHARACTER(t):
    r"'\w'"
    return t

# Para contar el numero de lineas 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored tokens
t_ignore = ' \t'

def t_comment_error(t):
	#r'/\*[\w\W/\*]*?'
	r'/\*.*[/\*|\*/]+.*\*/'
	print "Linea %d Comentario indeterminado. '%s'" % (t.lexer.lineno,t.value[0:2])

def t_comments(t):
	r'/\*[\w\W]*?\*/'
	t.lexer.lineno += t.value.count('\n')

# Una regla para manejar errores.
def t_error(t):
    print "Linea %d." % (t.lexer.lineno,) + "",
    if t.value[0] == '"':
        print "Indeterminado string."
        if t.value.count('\n') > 0:
            t.lexer.skip(t.value.index('\n'))
    elif t.value[0:2] == '/*':
        print "Comentario indeterminado. '%s'" % (t.value[0:2])
    else:
        print "Caracter ilegal '%s'" % t.value[0]
        t.lexer.skip(1)

# Funcion principal
def run_lexer():
    """
	Funcion principal, lee un archivo desde la entrada estardar y devuelve los tokens
    """

    import sys
    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()
    strings='''
    '''
    for i in lines:
        strings += i
    lex.input(strings)
    while 1:
        token = lex.token()       # Get a token
        if not token: break        # No more tokens
        print "(%s,'%s',%d)" % (token.type, token.value, token.lineno-1)

lex.lex()
symtab.new_scope()

if __name__ == '__main__':
    run_lexer()

