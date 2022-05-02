import ply.lex as lex
import tokenrules

lexer = lex.lex(module=tokenrules)

if __name__ == "__main__":
    
    with open("test.rbon","r") as f:
        data = f.read()

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)