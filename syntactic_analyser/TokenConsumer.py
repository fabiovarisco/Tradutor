'''
Created on 17 de mai de 2018

@author: I844141
'''

class TokenConsumer(object):
    '''
    Helper class that stores an array of tokens and consumes them or throws an error if there's one
    '''


    def __init__(self, tokens):
        '''
        Instantiates a Token Consumer
        -------------
        Parameters
        -------------
            tokens: array of tokens to be consumed
        '''
        self.tokens = tokens
        self.pos = 0
        self.checkpoints = []
    
    def hasNext(self):
        return self.pos < len(self.tokens)
    
    def next(self):
        '''
        Advances the pointer to the next token in the list
        '''
        self.pos += 1
        
    def getCurrent(self):
        '''
        Returns the current token
        '''
        return self.tokens[self.pos].value
    
    def getCurrentType(self):
        '''
        Returns the type of the current token
        '''
        return self.tokens[self.pos].token_type
    
    def getNextTokenType(self):
        return self.tokens[self.pos + 1].token_type
    
    def consume(self, token_type):
        '''
        Checks if the current token is of the type provided as parameter.
        If it is, advances to the next token.
        Otherwise, throws an error. 
        '''
        if (self.pos >= len(self.tokens)):
            self.endOfFileError(token_type)
        if (self.getCurrentType() == token_type):
            self.next()
        else:
            self.error(token_type)
            
    def checkpoint(self):
        self.checkpoints.append(self.pos)
    
    def revertToCheckpoint(self):
        self.pos = self.checkpoints.pop()
    
    def error(self, token_type):
        print('Was expecting ' + token_type + ", but got " + self.getCurrent() + " instead.")
        raise Exception("Compilation error found on token: " + self.getCurrent())
    
    def endOfFileError(self, token_type):
        print('Was expecting ' + token_type + ", but reached end of file.")
        raise Exception('Was expecting ' + token_type + ", but reached end of file.")