import ply.yacc as yacc
import rbonlex
import pprint
import warnings

from tokenrules import tokens

pp = pprint.PrettyPrinter(indent=2)

start = "elements"
variables = {}

def p_elementname(p):
    '''elementname : ID
                   | UNDERSCORE
    '''
    p[0] = p[1]

def p_args(p):
    '''args : objects
            | empty
    '''
    p[0] = p[1]

def p_objects(p):  # TODO: change naming
    ''' objects : object COMMA objects
                | object COMMA
                | object
    '''
    lp = len(p)
    if lp == 2:
        p[0] = p[1]
    elif lp == 3:
        p[0] = p[1]
    elif lp == 4:
        p[0] = {**p[1], **p[3]}

def p_object(p):
    '''object : ID COLON objectvalue
    '''

    # TODO:

    emptydict = {}

    if len(p) == 4:
        emptydict[p[1]] = p[3]
        p[0] = emptydict

    elif len(p) == 6:
        emptydict[p[1] + p[2] + p[3]] = p[5]
        p[0] = emptydict

def p_objectvalue(p):
    ''' objectvalue : NUMBER unit
                    | STRING
                    | NUMBER
    '''
    lp = len(p)
    if lp == 2:
        p[0] = str(p[1]).replace('\"','')
    elif lp == 3:
        p[0] = p[1] + p[2]

def p_unit(p):
    '''unit : PT
            | PX
            | CM
    '''
    p[0] = p[1]

def p_boolean(p):
    ''' boolean : TRUE
                | FALSE
    '''
    p[0] = p[1]

def p_empty(p):
    'empty : '
    pass

def p_show(p):
    ''' show : SHOW LBRACKET ID RBRACKET
    '''
    p[0] = variables[p[3]]

def p_error(p):
    print(f"Syntax error in input! {p}")

def p_elements(p):
    ''' elements : element
                 | element elements
                 | show
                 | show elements
                 
    '''
    if len(p) == 2:
        if p[1] is not None:
            p[0] = [p[1]]
    elif len(p) == 3:
        if p[1] is not None:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = p[2]


def p_element(p):
    ''' element : document
                | paragraph
                | varstring
    '''
    p[0] = p[1]

def p_returnableelements(p):
    ''' returnableelements : paragraph
    '''
    p[0] = p[1]


def p_document(p):
    ''' document : DOCUMENT elementname EQUAL LPAREN args RPAREN LCURLY docreturn RCURLY'''
    elementdict = {"type": p[1], "name": p[2], "args": p[5], "return": p[8]}

    variables[p[2]] = elementdict

def p_docreturn(p):
    '''docreturn : string
                | string docreturn
                | returnableelements
                | returnableelements docreturn
                | show
                | show docreturn
                | empty
    '''

    lp = len(p)
    if lp == 2:

        p[0] = [p[1]]
    elif lp == 3:
        p[0] = [p[1]] + p[2]


def p_paragraph(p):
    ''' paragraph : PARAGRAPH elementname EQUAL LPAREN args RPAREN LCURLY string RCURLY
    '''

    elementdict = {"type": p[1], "name": p[2], "args": p[5], "return": p[8]}

    variables[p[2]] = elementdict

def p_string(p):
    # TODO: try except
    # FIXME: concat string and other types i.e string + paragraph
    '''string : STRING
                | STRING PLUS string
                | show
                | show PLUS string
    '''
    if len(p) == 4:
        p[0] = str(p[1]).replace('\"','') + p[3]
    elif len(p) == 2:
        p[0] = str(p[1]).replace('\"','')


def p_varstring(p):
    ''' varstring : STR elementname EQUAL STRING 
    '''
    variables[p[2]] = str(p[4]).replace('\"','')

parser = yacc.yacc()

with open("./example/example.rbon", "r") as f:
    data = f.read()

result = parser.parse(data,debug=0)
pp.pprint(result)
