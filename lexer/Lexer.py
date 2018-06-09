'''
Created on 22 de mar de 2018

@author: I844141
'''
from lexer.TokenModule import Token
import re

WHITESPACE = 'whitespace'
BEGIN_COMMENT_BLOCK = 'BEGIN_COMMENT_BLOCK'
END_COMMENT_BLOCK = 'END_COMMENT_BLOCK'
COMMENT_LINE = 'COMMENT_LINE'

class Lexer(object):
    '''
    Lexical Analyzer for language C
    '''
    
    def __init__(self, text):
        self.text = text
        self.tokens = []
        #self.keywords = ['void', 'return', '#include',
        #                 'if', 'else', 'do', 'while', 'switch', 'case', 'break', 'for', 
        #                 'new', 'NewArray', 'ReadLine', 'ReadInteger']
        
        self.keywords = ['def', 'if', 'else', 'while', 'return', 'break', 'continue', 'true',  'false',
                         'for', 'callout', 'class', 'interface', 'extends', 'implements', 'new', 'this', 'string', 
                         'float', 'double', 'null']

        self.variable_types = ['int', 'void', 'bool']

        token_specification = [(WHITESPACE, r'\s+'),
                               (Token.TYPE_STRING_LITERAL, r'".*"'),
                               (Token.TYPE_ID, r'[A-Za-z][A-Za-z0-9_]*'),
                               #(BEGIN_COMMENT_BLOCK, r'\/\*'),
                               #(END_COMMENT_BLOCK, r'\*\/'),
                               (COMMENT_LINE, r'\/\/.*'),
                               #(Token.TYPE_ARIT_OP, r'\+|-|\*|/'),
                               #(Token.TYPE_FLOAT, r'\d+\.\d+'),
                               (Token.TYPE_HEX, r'0x[0-9a-fA-F]*'),
                               (Token.TYPE_NUM, r'\d+(\.\d+)?'),
                               (Token.TYPE_PAREN_L, r'\('),
                               (Token.TYPE_PAREN_R, r'\)'),
                               (Token.TYPE_BRACE_L, r'\{'),
                               (Token.TYPE_BRACE_R, r'\}'),
                               (Token.TYPE_BRACKET_L, r'\['),
                               (Token.TYPE_BRACKET_R, r'\]'),
                               (Token.TYPE_UNARY_OP, r'!'),
                               (Token.TYPE_BINARY_OP, r'\*|/|%|\+|-|<|<=|>=|>|==|!=|&&|\|\|'),
                               (Token.TYPE_EQUAL, r'='),
                               (Token.TYPE_COMMA, r','),
                               (Token.TYPE_SEMICOLON, r';')
                               #(Token.TYPE_RELATIONAL_OP, r'<|<=|==|!=|>=|>'),
                               #(Token.TYPE_LOGICAL_OP, r'\|\||&&'),
                               #(Token.TYPE_INCLUDE, r'((?i)\#include).*'),

                               ]
        
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    def evaluate(self):
        line_num = 1
        #is_comment = False
        for line in self.text:
            for mo in re.finditer(self.tok_regex, line):
                kind = mo.lastgroup
                value = mo.group(kind)
                #if (kind == BEGIN_COMMENT_BLOCK):
                #    is_comment = True
                if (kind != WHITESPACE and kind != COMMENT_LINE): # and is_comment == False):
                    if (kind == Token.TYPE_ID):
                        if (value in self.keywords):
                            kind = Token.TYPE_RESERVED_WORD
                        elif (value in self.variable_types):
                            kind = Token.TYPE_RESERVED_VAR_TYPE
                    self.tokens.append(Token(kind, value, line_num, mo.start()))
                #if (kind == END_COMMENT_BLOCK):
                #    is_comment = False
            line_num += 1
    def printTokens(self):
        for t in self.tokens:
            print(t)

if __name__ == "__main__":
    with open('entrada.txt','r') as f:
        text = f.readlines()
        text = [l.strip() for l in text]
        
    lexer = Lexer(text)
    lexer.evaluate()
    lexer.printTokens()
    