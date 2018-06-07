'''
Created on 17 de mai de 2018

@author: I844141
'''
from syntactic_analyser.TokenConsumer import TokenConsumer
from lexer.TokenModule import Token
from lexer.Lexer import Lexer
from syntactic_analyser.SyntacticException import SyntacticException

class SyntacticAnalyser(object):
    '''
    Helper class that defines a recursive top-down syntactic analyser for the Decaf language. 
    '''

    VARIABLE_TYPE = ['int', 'double', 'bool', 'string']
    
    def __init__(self, tokens):
        '''
        Instantiantes a new analyser
        '''
        self.tokenConsumer = TokenConsumer(tokens)
        
    
    def analyse(self):   
        self.Program()
        
    def Program(self):
        while (self.tokenConsumer.hasNext()):
            self.Decl()
            
    def Decl(self):
        if (self.checkVariableOrFuncDecl()):
            self.VariableOrFuncDecl()
       
    def checkVariableOrFuncDecl(self):
        # If starts with a 'void' or a type declaration, it should be either VariableDecl or FunctionDecl
        return (self.tokenConsumer.getCurrent() == 'void' or self.isOfVarType())
    
    def VariableOrFuncDecl(self):
        try:
            self.tokenConsumer.checkpoint()
            self.VariableDecl()
        except (SyntacticException) as exception: 
            print(exception)
            self.tokenConsumer.revertToCheckpoint()
            try:
                self.FunctionDecl()
            except (SyntacticException) as exception:     
                print(exception)
    
    def VariableDecl(self):
        self.Variable()
        self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
    
    def Variable(self):
        self.Type()
        self.tokenConsumer.consume(Token.TYPE_ID)
    
    def isOfVarType(self):
        return self.tokenConsumer.getCurrentType() == Token.TYPE_RESERVED_VAR_TYPE or self.tokenConsumer.getCurrentType() == Token.TYPE_ID
    
    def Type(self):
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_RESERVED_VAR_TYPE):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_VAR_TYPE)
        else:
            self.tokenConsumer.consume(Token.TYPE_ID)
            
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_BRACKET_L):
            self.tokenConsumer.consume(Token.TYPE_BRACKET_L)
            self.tokenConsumer.consume(Token.TYPE_BRACKET_R)
    
    def FunctionDecl(self):
        if (self.tokenConsumer.getCurrent() == 'void'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
        else :
            self.tokenConsumer.consume(Token.TYPE_RESERVED_VAR_TYPE)
        self.tokenConsumer.consume(Token.TYPE_ID)
        self.tokenConsumer.consume(Token.TYPE_PAREN_L)
        #self.Formals()
        self.tokenConsumer.consume(Token.TYPE_PAREN_R)
        #self.StmtBlock()
        
    def Formals(self):
        try: 
            self.Variable()
            while (self.tokenConsumer.hasNext()):
                if (self.tokenConsumer.getNextTokenType() == Token.TYPE_COMMA):
                    self.tokenConsumer.consume(Token.TYPE_COMMA)
                    self.Variable()
                else:
                    break
        except: 
            pass
    
    def ClassDecl(self):
        if (self.tokenConsumer.getCurrent() == 'class'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_ID)
            if (self.tokenConsumer.getNextTokenType() == 'extends'):
                self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
                self.tokenConsumer.consume(Token.TYPE_ID)
            while (self.tokenConsumer.hasNext()):
                if (self.tokenConsumer.getNextTokenType() == 'implements'):
                    self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
                    self.tokenConsumer.consume(Token.TYPE_ID)
                    while (self.tokenConsumer.hasNext()):
                            if (self.tokenConsumer.getNextTokenType() == Token.TYPE_COMMA):
                                self.tokenConsumer.consume(Token.TYPE_COMMA)
                                self.tokenConsumer.consume(Token.TYPE_ID)
                            else:
                                break
                else:
                    break
            self.tokenConsumer.consume(Token.TYPE_BRACE_L)
            while (self.tokenConsumer.hasNext()):
                try: 
                    self.Field()
                    pass
                except:
                    break
            self.tokenConsumer.consume(Token.TYPE_BRACE_R)
        else:
            self.tokenConsumer.error("class")
    
    def Field(self):
        if (self.checkVariableOrFuncDecl()):
            self.VariableOrFuncDecl()
        else:
            self.tokenConsumer.error("Variable or Function Declaration")

    def InterfaceDecl(self):
        if (self.tokenConsumer.getCurrent() == 'interface'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_ID)
            self.tokenConsumer.consume(Token.TYPE_BRACE_L)
            while (self.tokenConsumer.hasNext()):
                try: 
                    self.Prototype()
                except:
                    break
                
            self.tokenConsumer.consume(Token.TYPE_BRACE_R)
        else:
            self.tokenConsumer.error('interface')
    
    def Prototype(self):
        if (self.tokenConsumer.getCurrent() == 'void'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
        else:
            self.Type()
        
        self.tokenConsumer.consume(Token.TYPE_ID)
        self.tokenConsumer.consume(Token.TYPE_PAREN_L)
        self.Formals()
        self.tokenConsumer.consume(Token.TYPE_PAREN_R)
        self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
        
    def StmtBlock(self):
        self.tokenConsumer.consume(Token.TYPE_BRACE_L)
        while (self.tokenConsumer.hasNext()):
            try:
                self.VariableDecl()
            except:
                break
        while (self.tokenConsumer.hasNext()):
            try:
                self.Stmt()
            except:
                break
        self.tokenConsumer.consume(Token.TYPE_BRACE_R)
    
    def Stmt(self):
        pass
        #TODO Impl
        
    def IfStmt(self):
        if (self.tokenConsumer.getCurrent() == 'if'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            self.Stmt()
            while (self.tokenConsumer.hasNext()):
                if (self.tokenConsumer.getCurrent() == 'else'):
                    self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
                    self.Stmt()
                else: 
                    break
        else:
            self.tokenConsumer.error('if')
    
    def WhileStmt(self):
        if (self.tokenConsumer.getCurrent() == 'while'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            self.Stmt()   
        else:
            self.tokenConsumer.error('while')
    
    def ForStmt(self):
        if (self.tokenConsumer.getCurrent() == 'for'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            try:
                self.Expr()
            except:
                pass
            self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
            try:
                self.Expr()
            except:
                pass
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            self.Stmt()   
        else:
            self.tokenConsumer.error('for')
            
    def ReturnStmt(self):
        if (self.tokenConsumer.getCurrent() == 'return'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            try:
                self.Expr()
            except:
                pass
        else:
            self.tokenConsumer.error('return')
    
    def BreakStmt(self):
        if (self.tokenConsumer.getCurrent() == 'break'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
        else:
            self.tokenConsumer.error('break')
            
    def PrintStmt(self):
        if (self.tokenConsumer.getCurrent() == 'print'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            while (self.tokenConsumer.hasNext()):
                try:
                    self.Expr()
                except:
                    pass
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
        else:
            self.tokenConsumer.error('break')
    
    def Expr(self):
        if (self.tokenConsumer.getCurrent() == 'this'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            return
        if (self.tokenConsumer.getCurrent() == 'ReadInteger' or 
            self.tokenConsumer.getCurrent() == 'ReadLine'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            return
        if (self.tokenConsumer.getCurrent() == 'new'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_ID)
            return
        if (self.tokenConsumer.getCurrent() == 'NewArray'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_COMMA)
            self.Type()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            return
        
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_PAREN_L):
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            return
        
        try:
            self.LValue()
            try:
                self.tokenConsumer.consume(Token.TYPE_EQUAL)
                self.Expr()
            except:
                pass  
        except:
            pass

    def LValue(self):
        pass
        #TODO Impl
        
if __name__ == "__main__":
    with open('../sample1.decaf','r') as f:
        text = f.readlines()
        text = [l.strip() for l in text]
        
    lexer = Lexer(text)
    lexer.evaluate()
    lexer.printTokens()
    
    analyser = SyntacticAnalyser(lexer.tokens)
    analyser.analyse()
    