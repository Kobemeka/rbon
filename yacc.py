import ply.yacc as yacc
import rbonlex
import pprint
import warnings

from tokenrules import tokens

pp = pprint.PrettyPrinter(indent=2)

# TODO: None control

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

def p_funcargs(p):
    '''funcargs : funcobjects
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

def p_funcobjects(p):
    ''' funcobjects : thisobj COMMA funcobjects
                | thisobj COMMA
                | thisobj
    '''
    lp = len(p)
    if lp == 2:
        p[0] = [p[1]]
    elif lp == 3:
        p[0] = [p[1]]
    elif lp == 4:
        p[0] = [p[1]] + p[3]

def p_object(p):
    '''object : ID COLON objectvalue
    '''

    emptydict = {}

    emptydict[p[1]] = p[3]
    p[0] = emptydict

def p_objectvalue(p):
    ''' objectvalue : NUMBER unit
                    | STRING
                    | NUMBER
                    | boolean
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
    ''' show : SHOW LBRACKET ids RBRACKET
    '''
    if p[3] in variables:
        p[0] = {"type": p[1], "name": p[3], "shows": variables[p[3]]}
    else:
        p[0] = {"type": p[1], "name": p[3], "shows": p[3]}

def p_ids(p):
    '''ids : ID
            | thisobj
    '''
    p[0] = p[1]
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
                | equation
                | function
    '''
    p[0] = p[1]

def p_returnableelements(p):
    ''' returnableelements : paragraph
                            | call
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

def p_equation(p):
    ''' equation : EQUATION elementname EQUAL LPAREN args RPAREN LCURLY string RCURLY
    '''
    elementdict = {"type": p[1], "name": p[2], "args": p[5], "return": p[8]}

    variables[p[2]] = elementdict

def p_function(p):
    ''' function : FUNCTION elementname EQUAL LPAREN funcargs RPAREN LCURLY funcreturn RCURLY
    '''
    elementdict = {"type": p[1], "name": p[2], "args": p[5], "return": p[8]}

    variables[p[2]] = elementdict

def p_funcobject(p):
    '''funcobject : show
                    | show COMMA funcobject
                    | string
                    | string COMMA funcobject
                    | element
                    | element COMMA funcobject
                    | ID
                    | empty
    '''
    lp = len(p)
    if lp == 2:
        p[0] = [p[1]]
    elif lp == 4:
        p[0] = [p[1]] + p[3]
    # emptydict = {}

    # emptydict[p[3]] = p[1] + p[2] + p[3]
    # p[0] = emptydict

def p_funcreturn(p):
    # TODO: FIX RETURN
    '''funcreturn : RETURN show
                    | RETURN show funcreturn
                    | RETURN thisobj
                    | RETURN thisobj funcreturn
                    | RETURN call
                    | RETURN call funcreturn
    '''
    lp = len(p)

    if lp == 3:
        p[0] = [p[2]]
    elif lp == 4:
        p[0] = [p[2]] + p[3]

def p_call(p):
    '''call : CALL LBRACKET ids RBRACKET LBRACKET funcobject RBRACKET
    '''
    p[0] = {"type": p[1], "name": p[3], "args": p[6]}
    # variables[p[3]] = {"func-name": p[3],"call-args":p[6]}

def p_thisobj(p):
    '''thisobj : THIS DOT ID
    '''
    p[0] = p[1] + p[2] + p[3]

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
