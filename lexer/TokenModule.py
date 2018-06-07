'''
Created on 22 de mar de 2018

@author: I844141
'''

class Token(object):
    '''
    Token object to be used by the Lexer. Indicates token_type, value and position in the code
    '''
    
    TYPE_RESERVED_VAR_TYPE = 'VARIABLE_TYPE'
    TYPE_RESERVED_WORD = 'RESERVED_WORD'
    TYPE_NUM = 'NUM'
    TYPE_ID = 'ID'
    TYPE_ARIT_OP = 'ARIT_OP'
    TYPE_EQ_OP = 'EQ_OP'
    TYPE_LOGICAL_OP = 'LOGIC_OP'
    TYPE_RELATIONAL_OP = 'RELATIONAL_OP'
    TYPE_STRING_LITERAL = 'STRING_LITERAL'
    TYPE_PAREN_L = 'L_PAREN'
    TYPE_PAREN_R = 'R_PAREN'
    TYPE_BRACKET_L = 'L_BRACKET'
    TYPE_BRACKET_R = 'R_BRACKET'
    TYPE_BRACE_L = 'L_BRACE'
    TYPE_BRACE_R = 'R_BRACE'
    TYPE_EQUAL = 'EQUAL'
    TYPE_COMMA = 'COMMA'
    TYPE_SEMICOLON = 'SEMICOLON'
    TYPE_INCLUDE = 'INCLUDE'

    def __init__(self, token_type, value, line = 0, position = 0):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.position = position
    
    def __str__(self):
        """String representation of the class instance.

        Examples:
            [NUM, 3]
            [ARIT_OP, +]
        """
        return '[{type}, {value}, {line}, {position}]'.format(
            type=self.token_type,
            value=repr(self.value),
            line=self.line,
            position=self.position
        )

    def __repr__(self):
        return self.__str__()