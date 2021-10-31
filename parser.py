# operand
#    ( Expr )
# #    ( Expr ) [ Expr ]...
#    operand?
#    number
# #    rational
# #    vector
# #    variable
# #    operand [ Expr ]...
#    unop Expr

# expr
#    operand
#    operand binop expr

# statement:
# #   var '=' Expr
#    Expr

# # are not yet implemented

from enum import Enum, auto
from math import sin, cos, exp, log

UNOPS = ['neg', 'sin', 'cos', 'exp', 'log']
BINOPS = ['+', '-', '*', '/', '^']

class Type(Enum):
    NUMBER = auto()
    UNOP = auto()
    BINOP = auto()
    LPAREN = auto()
    RPAREN = auto()

class Token():
    def __init__(self, type, str):
        self.type = type
        self.str = str

    def __str__(self):
        return '<' + self.str + ', ' + str(self.type) + '>'
    
    @staticmethod
    def tokenize(str):
        tokens = []
        tok = ''
        currentNum = False
        for c in str.strip():
            if c.isspace():
                if currentNum:
                    currentNum = False
                    tokens.append(Token(Type.NUMBER, tok))
                    tok = ''
                if tok != '':
                    raise ValueError('Parsing error during Tokenize.')
                else:
                    continue
            tok = (tok + c).lower()
            if is_num(tok):
                currentNum = True
            elif currentNum:
                currentNum = False
                tokens.append(Token(Type.NUMBER, tok[:-1]))
                tok = tok[-1]
            if tok in UNOPS:
                tokens.append(Token(Type.UNOP, tok))
                tok = ''
            elif tok in BINOPS:
                tokens.append(Token(Type.BINOP, tok))
                tok = ''
            elif tok == '(':
                tokens.append(Token(Type.LPAREN, tok))
                tok = ''
            elif tok == ')':
                tokens.append(Token(Type.RPAREN, tok))
                tok = ''
        if tok != '':
            if currentNum:
                tokens.append(Token(Type.NUMBER, tok))
            else:
                raise ValueError('Parsing error during Tokenize.')
        return tokens
                    
def is_num(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def parseStatement(tokens):
    return parseExpression(tokens)

def parseExpression(tokens):
    result = parseOperand(tokens)
    if len(tokens) > 0:
        if tokens[0].type == Type.BINOP:
            op = tokens.pop(0)
            secondResult = parseExpression(tokens)
            return bineval(op, result, secondResult)
        else:
            return result
    else:
        return result

def parseOperand(tokens):
    if len(tokens) > 0:
        if tokens[0].type == Type.NUMBER:
           tok = tokens.pop(0)
           return float(tok.str)
        elif tokens[0].type == Type.UNOP:
            op = tokens.pop(0)
            result = parseExpression(tokens)
            return uneval(op, result)
        elif tokens[0].type == Type.LPAREN:
            tokens.pop(0)
            result = parseExpression(tokens)
            if tokens[0].type == Type.RPAREN:
                tokens.pop(0)
            else:
                raise ValueError('Parsing error during Evaluation.')
            return result
    else:
        raise ValueError('Parsing error during Evaluation.')

def uneval(op, x):
    if op.str == UNOPS[0]:
        return -1 * x
    elif op.str == UNOPS[1]:
        return sin(x)
    elif op.str == UNOPS[2]:
        return cos(x)
    elif op.str == UNOPS[3]:
        return exp(x)
    elif op.str == UNOPS[4]:
        return log(x)
        
def bineval(op, x, y):
    if op.str == BINOPS[0]:
        return x + y
    if op.str == BINOPS[1]:
        return x - y
    if op.str == BINOPS[2]:
        return x * y
    if op.str == BINOPS[3]:
        return x / y
    if op.str == BINOPS[4]:
        return x ** y 

def help():
    print('Unary Operators apply to everything right of them, available are:')
    for op in UNOPS:
        print('\'' + op + '\', ', end='')
    print()    
    print('Binary Operators apply to the operand to the left and everything right of them, available are:')
    for op in BINOPS:
        print('\'' + op + '\', ', end='')
    print()
    print('Type \'exit\' to exit.')
      
def main():
    while True:
        line = input()
        if line.lower() == 'exit':
            exit()
        elif line.lower() == 'help':
            help()
        else:
            try:
                inTokens = Token.tokenize(line)
                result = parseExpression(inTokens)
                print(result)
            except:
                print('Error parsing \'' + line + '\'. Type \'help\' for help.')

if __name__ == '__main__':
    main()