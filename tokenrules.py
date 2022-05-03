# TODO: Count equations

reserved = {
    # VAR

    'var' : 'VAR',
    'show' : 'SHOW',
    'call' : 'CALL',

    # OPTIONS

    ## UNITS
    'pt': 'PT',
    'px': 'PX',
    'cm': 'CM',

    ## STYLES
    # 'fontsize': 'FONTSIZE',

    # TYPES
    'Document': 'DOCUMENT',
    'Table': 'TABLE',
    'TableItem': 'TABLEITEM',
    'Paragraph': 'PARAGRAPH',
    'Equation': 'EQUATION',
    'Function': 'FUNCTION',

    # CONDITION
    # 'if': 'IF',
    # 'then': 'THEN',
    # 'else': 'ELSE',

    # BOOLEANS

    'True': 'TRUE',
    'False': 'FALSE',

    # FUNCTION
    'Return': 'RETURN',

    # Special Functions

    # 'ToString': 'TOSTRING', # not sure
    # 'Sup': 'SUP',
    # 'Sub': 'SUB',
    'Str': 'STR',

    # Keywords

    'this': 'THIS',
}

tokens = list(reserved.values()) + [
    # LOGIC OPS
    # 'CEQUAL',

    # ARITHMETIC OPS
    'PLUS',
    # 'MINUS',
    # 'TIMES',
    # 'DIVIDE',

    # ASIGNMENT
    'EQUAL',

    # PUNCTUATION MARKS

    ## PARENTHESES
    'LPAREN',
    'RPAREN',
    'RCURLY',
    'LCURLY',
    'RBRACKET',
    'LBRACKET',

    ## 
    'DOT',
    'COMMA',
    'COLON',
    # 'SEMICOLON',
    'UNDERSCORE',

    # TYPES

    'ID',
    'NUMBER',
    'STRING',
]

# Regular expression rules for simple tokens

t_VAR = r'var'
t_SHOW = r'show'
t_CALL = r'call'

t_PT = r'pt'
t_PX = r'px'
t_CM = r'cm'

# t_FONTSIZE = r'fontsize'

t_DOCUMENT = r'Document'
t_TABLE = r'Table'
t_TABLEITEM = r'TableItem'
t_PARAGRAPH = r'Paragraph'
t_EQUATION = r'Equation'
t_FUNCTION = r'Function'

# t_IF = r'if'
# t_THEN = r'then'
# t_ELSE = r'else'

t_TRUE = r'True'
t_FALSE = r'False'

t_RETURN = r'Return'

# t_TOSTRING = r'ToString'
# t_SUP = r'Sup'
# t_SUB = r'Sub'

t_THIS = r'this'

t_STR = r'Str'

# t_CEQUAL = r'\=\='

t_PLUS = r'\+'
# t_MINUS = r'\-'
# t_TIMES = r'\*'
# t_DIVIDE = r'\/'

t_EQUAL = r'\='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_DOT = r'\.'
t_COMMA = r'\,'
t_COLON = r'\:'
# t_SEMICOLON = r'\;'
t_UNDERSCORE = r'\_'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"(\\.|[^"\\])*\"'
    t.value = str(t.value)
    return t

# def t_LIST(t):
#     r'\"(\\.|[^"\\])*\"'
#     t.value = str(t.value)
#     return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input, token):
    # TODO: find column number
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_COMMENT(t):
     r'\#.*'
     pass

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal Character {t.value[0]} at position {t.lexpos} and at line {t.lineno}")
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
