'''
Created on 26 de mai de 2018

@author: I844141
'''

class SyntacticException(Exception):
    '''
    Represents a syntatic error in the input code to the compiler. 
    '''


    def __init__(self, expected_token_type, current_token_type, current_token, line, column):
        '''
        Constructor for Syntactic Exception
        '''
        self.expectedToken = expected_token_type
        self.currentTokenType = current_token_type
        self.currentToken = current_token
        self.line = line
        self.column = column
        super(expected_token_type, current_token, current_token, line, column)
        