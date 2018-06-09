'''
Created on 17 de mai de 2018

@author: I844141
'''
from syntactic_analyser.TokenConsumer import TokenConsumer
from lexer.TokenModule import Token
from lexer.Lexer import Lexer
from syntactic_analyser.SyntacticException import SyntacticException

VARIABLE_TYPE = ['int', 'void', 'bool']
STATEMENT_START_KEYWORDS = ['if', 'while', 'return', 'break', 'continue']

class SyntacticAnalyser(object):
    '''
    Helper class that defines a recursive top-down syntactic analyser for the Decaf language. 
    '''
    
    def __init__(self, tokens):
        '''
        Instantiantes a new analyser
        '''
        self.tokenConsumer = TokenConsumer(tokens)
        
    
    def analyse(self):   
        self.Program()
        print('Input program is correct. Syntactic analysis was successful!')
        
    def Program(self):
        '''
        Implements the production: Program -> (Var|Func)*
        '''
        while (self.tokenConsumer.hasNext()):
            if (self.checkVarDecl()):
                self.Variable()
            elif (self.checkFuncDecl()):
                self.FunctionDecl()
            else: 
                self.tokenConsumer.error(" function declaration or a variable declaration.")
    
    def checkVarDecl(self):
        ''' 
        Check if the function starts with a variable declaration
        returns true if the current token is a type keyword
        '''
        return self.isOfVarType()
    
    def isOfVarType(self):
        '''
        Checks if the current token is a variable type keyword
        return true if the current token is a variable type keyword. False, otherwise.
        '''
        return self.tokenConsumer.getCurrentType() == Token.TYPE_RESERVED_VAR_TYPE #or self.tokenConsumer.getCurrentType() == Token.TYPE_ID
    
    def checkParameterList(self):
        ''' 
        Checks if the next declaration is a parameter list.
        returns true if the current token is a type keyword
        '''
        return self.isOfVarType()
    
    def checkFuncDecl(self):
        '''
        Checks if the next statement is a function declaration.
        returns true if the current token is 'def', which means it's the start of a function declaration. False, otherwise. 
        '''
        return self.tokenConsumer.getCurrent() == 'def'
    
    def Variable(self):
        '''
        Implements the production: Var -> Type ID ('[' DEC ']')? ';'
        '''
        self.Type()
        self.tokenConsumer.consume(Token.TYPE_ID)
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_BRACKET_L):
            self.tokenConsumer.consume(Token.TYPE_BRACKET_L)
            self.tokenConsumer.consume(Token.TYPE_NUM)
            self.tokenConsumer.consume(Token.TYPE_BRACKET_R)
        self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
    
    def Type(self):
        '''
        Implements the production: Type -> int | bool | void
        '''
        self.tokenConsumer.consume(Token.TYPE_RESERVED_VAR_TYPE)
    
    
    def FunctionDecl(self):
        '''
        Implements the production: Func -> def Type ID '(' ParamList? ')' Block
        '''
        if (self.tokenConsumer.getCurrent() == 'def'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
        else:
            self.tokenConsumer.error('def')
        self.Type()
        self.tokenConsumer.consume(Token.TYPE_ID)
        self.tokenConsumer.consume(Token.TYPE_PAREN_L)
        if (self.checkParameterList()):
            self.ParamList()
        self.tokenConsumer.consume(Token.TYPE_PAREN_R)
        self.Block()
    
    def ParamList(self):
        '''
        Implements the production: ParamList -> Type ID (',' Type ID)*
        '''
        self.Type()
        self.tokenConsumer.consume(Token.TYPE_ID)
        while (self.tokenConsumer.getCurrentType() == Token.TYPE_COMMA):
            self.tokenConsumer.consume(Token.TYPE_COMMA)
            self.Type()
            self.tokenConsumer.consume(Token.TYPE_ID)
    
    def Block(self):
        '''
        Implements the production: Block -> { Var* Stmt* }
        '''
        self.tokenConsumer.consume(Token.TYPE_BRACE_L)
        while (self.checkVarDecl()):
            self.Variable()
        while (self.checkStatementDecl()):
            self.Stmt()
        self.tokenConsumer.consume(Token.TYPE_BRACE_R)
    
    def checkStatementDecl(self):
        '''
        Checks if the next declaration will be a statement declaration
        returns true if the current token is one of the following ['if', 'while', 'return', 'break', 'continue'] or if the next token is an identifier
        '''
        return (self.tokenConsumer.getCurrent() in STATEMENT_START_KEYWORDS) or self.tokenConsumer.getCurrentType() == Token.TYPE_ID
    
    def Stmt(self):
        '''
        Implements the following production: Stmt -> Loc '=' Expr ';' | FuncCall ';' | if '(' Expr ')' Block ( else Block )?
                            | while '(' Expr ')' Block | return Expr? ';' | break ';' | continue ';'
        '''
        if (self.tokenConsumer.getCurrent() == 'if'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            self.Block()
            if (self.tokenConsumer.getCurrent() == 'else'):
                self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
                self.Block()
        elif (self.tokenConsumer.getCurrent() == 'while'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            self.Block()
        elif (self.tokenConsumer.getCurrent() == 'return'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            if (self.tokenConsumer.getCurrentType() != Token.TYPE_SEMICOLON):
                self.Expr()
            self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
        elif (self.tokenConsumer.getCurrent() == 'break' or self.tokenConsumer.getCurrent() == 'continue'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
            self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
        else: 
            self.tokenConsumer.checkpoint()
            self.tokenConsumer.consume(Token.TYPE_ID)
            if (self.tokenConsumer.getCurrentType() == Token.TYPE_PAREN_L):
                self.tokenConsumer.revertToCheckpoint()
                self.FuncCall()
                self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
            else:
                self.tokenConsumer.revertToCheckpoint()
                self.Loc()
                self.tokenConsumer.consume(Token.TYPE_EQUAL)
                self.Expr();
                self.tokenConsumer.consume(Token.TYPE_SEMICOLON)

    def Loc(self):
        '''
        Implements the production: Loc -> ID ('[' Expr ']')?
        '''
        self.tokenConsumer.consume(Token.TYPE_ID)
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_BRACKET_L):
            self.tokenConsumer.consume(Token.TYPE_BRACKET_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_BRACKET_R)
            
    
    def FuncCall(self):
        '''
        Implements the production: FuncCall -> ID '(' ArgList? ')'  
        '''
        self.tokenConsumer.consume(Token.TYPE_ID)
        self.tokenConsumer.consume(Token.TYPE_PAREN_L)
        if (self.tokenConsumer.getCurrentType() != Token.TYPE_PAREN_R):
            self.ArgList()
        self.tokenConsumer.consume(Token.TYPE_PAREN_R)
    
    def ArgList(self):
        '''
        Implements the production: ArgList -> Expr (',' Expr )*
        '''
        self.Expr()
        while (self.tokenConsumer.getCurrentType() == Token.TYPE_COMMA):
            self.tokenConsumer.consume(Token.TYPE_COMMA)
            self.Expr()
    
    def checkLiteral(self):
        return (self.tokenConsumer.getCurrent() == 'true' or self.tokenConsumer.getCurrent() == 'false' 
                or self.tokenConsumer.getCurrentType() == Token.TYPE_STRING_LITERAL 
                or self.tokenConsumer.getCurrentType() == Token.TYPE_HEX
                or self.tokenConsumer.getCurrentType() == Token.TYPE_NUM)
        
    def Lit(self):
        '''
        Implements the production: Lit -> DEC | HEX | STR | true | false
        '''
        if (self.tokenConsumer.getCurrent() == 'true' or self.tokenConsumer.getCurrent() == 'false'):
            self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
        elif (self.tokenConsumer.getCurrentType() == Token.TYPE_STRING_LITERAL):
            self.tokenConsumer.consume(Token.TYPE_STRING_LITERAL)
        elif (self.tokenConsumer.getCurrentType() == Token.TYPE_NUM):
            self.tokenConsumer.consume(Token.TYPE_NUM)
        elif (self.tokenConsumer.getCurrentType() == Token.TYPE_HEX):
            self.tokenConsumer.consume(Token.TYPE_HEX)
        else:
            self.tokenConsumer.error('Literal (dec, hex, str, true or false)')
    
    def Expr2 (self):
        '''
        Implements the production: EXPR2 -> BINOP Expr EXPR2 | empty
        '''
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_BINARY_OP):
            self.tokenConsumer.consume(Token.TYPE_BINARY_OP)
            self.Expr()
            self.Expr2()
    
    def Expr(self): 
        '''
        Implements the production: Expr -> UNOP EXPR2 | '(' Expr ')' EXPR2 | Loc EXPR2 | FuncCall EXPR2 | Lit EXPR2
        '''
        if (self.tokenConsumer.getCurrentType() == Token.TYPE_UNARY_OP):
            self.tokenConsumer.consume(Token.TYPE_UNARY_OP)
            self.Expr2()
        elif (self.tokenConsumer.getCurrentType() == Token.TYPE_PAREN_L):
            self.tokenConsumer.consume(Token.TYPE_PAREN_L)
            self.Expr()
            self.tokenConsumer.consume(Token.TYPE_PAREN_R)
            self.Expr2()
        elif (self.checkLiteral()):
            self.Lit()
            self.Expr2()
        else: 
            self.tokenConsumer.checkpoint()
            self.tokenConsumer.consume(Token.TYPE_ID)
            if (self.tokenConsumer.getCurrentType() == Token.TYPE_PAREN_L):
                self.tokenConsumer.revertToCheckpoint()
                self.FuncCall()
                self.Expr2()
            else:
                self.tokenConsumer.revertToCheckpoint()
                self.Loc()
                self.Expr2()

#     def Formals(self):
#         try: 
#             self.Variable()
#             while (self.tokenConsumer.hasNext()):
#                 if (self.tokenConsumer.getNextTokenType() == Token.TYPE_COMMA):
#                     self.tokenConsumer.consume(Token.TYPE_COMMA)
#                     self.Variable()
#                 else:
#                     break
#         except: 
#             pass
#     
#     def ClassDecl(self):
#         if (self.tokenConsumer.getCurrent() == 'class'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_ID)
#             if (self.tokenConsumer.getNextTokenType() == 'extends'):
#                 self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#                 self.tokenConsumer.consume(Token.TYPE_ID)
#             while (self.tokenConsumer.hasNext()):
#                 if (self.tokenConsumer.getNextTokenType() == 'implements'):
#                     self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#                     self.tokenConsumer.consume(Token.TYPE_ID)
#                     while (self.tokenConsumer.hasNext()):
#                             if (self.tokenConsumer.getNextTokenType() == Token.TYPE_COMMA):
#                                 self.tokenConsumer.consume(Token.TYPE_COMMA)
#                                 self.tokenConsumer.consume(Token.TYPE_ID)
#                             else:
#                                 break
#                 else:
#                     break
#             self.tokenConsumer.consume(Token.TYPE_BRACE_L)
#             while (self.tokenConsumer.hasNext()):
#                 try: 
#                     self.Field()
#                     pass
#                 except:
#                     break
#             self.tokenConsumer.consume(Token.TYPE_BRACE_R)
#         else:
#             self.tokenConsumer.error("class")
#     
#     def Field(self):
#         if (self.checkVariableOrFuncDecl()):
#             self.VariableOrFuncDecl()
#         else:
#             self.tokenConsumer.error("Variable or Function Declaration")
# 
#     def InterfaceDecl(self):
#         if (self.tokenConsumer.getCurrent() == 'interface'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_ID)
#             self.tokenConsumer.consume(Token.TYPE_BRACE_L)
#             while (self.tokenConsumer.hasNext()):
#                 try: 
#                     self.Prototype()
#                 except:
#                     break
#                 
#             self.tokenConsumer.consume(Token.TYPE_BRACE_R)
#         else:
#             self.tokenConsumer.error('interface')
#     
#     def Prototype(self):
#         if (self.tokenConsumer.getCurrent() == 'void'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#         else:
#             self.Type()
#         
#         self.tokenConsumer.consume(Token.TYPE_ID)
#         self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#         self.Formals()
#         self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#         self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
#         
#     def StmtBlock(self):
#         self.tokenConsumer.consume(Token.TYPE_BRACE_L)
#         while (self.tokenConsumer.hasNext()):
#             try:
#                 self.VariableDecl()
#             except:
#                 break
#         while (self.tokenConsumer.hasNext()):
#             try:
#                 self.Stmt()
#             except:
#                 break
#         self.tokenConsumer.consume(Token.TYPE_BRACE_R)
#     
#     def Stmt(self):
#         pass
#         #TODO Impl
#         
#     def IfStmt(self):
#         if (self.tokenConsumer.getCurrent() == 'if'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             self.Expr()
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#             self.Stmt()
#             while (self.tokenConsumer.hasNext()):
#                 if (self.tokenConsumer.getCurrent() == 'else'):
#                     self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#                     self.Stmt()
#                 else: 
#                     break
#         else:
#             self.tokenConsumer.error('if')
#     
#     def WhileStmt(self):
#         if (self.tokenConsumer.getCurrent() == 'while'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             self.Expr()
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#             self.Stmt()   
#         else:
#             self.tokenConsumer.error('while')
#     
#     def ForStmt(self):
#         if (self.tokenConsumer.getCurrent() == 'for'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             try:
#                 self.Expr()
#             except:
#                 pass
#             self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
#             self.Expr()
#             self.tokenConsumer.consume(Token.TYPE_SEMICOLON)
#             try:
#                 self.Expr()
#             except:
#                 pass
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#             self.Stmt()   
#         else:
#             self.tokenConsumer.error('for')
#             
#     def ReturnStmt(self):
#         if (self.tokenConsumer.getCurrent() == 'return'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             try:
#                 self.Expr()
#             except:
#                 pass
#         else:
#             self.tokenConsumer.error('return')
#     
#     def BreakStmt(self):
#         if (self.tokenConsumer.getCurrent() == 'break'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#         else:
#             self.tokenConsumer.error('break')
#             
#     def PrintStmt(self):
#         if (self.tokenConsumer.getCurrent() == 'print'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             while (self.tokenConsumer.hasNext()):
#                 try:
#                     self.Expr()
#                 except:
#                     pass
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#         else:
#             self.tokenConsumer.error('break')
#     
#     def Expr(self):
#         if (self.tokenConsumer.getCurrent() == 'this'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             return
#         if (self.tokenConsumer.getCurrent() == 'ReadInteger' or 
#             self.tokenConsumer.getCurrent() == 'ReadLine'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#             return
#         if (self.tokenConsumer.getCurrent() == 'new'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_ID)
#             return
#         if (self.tokenConsumer.getCurrent() == 'NewArray'):
#             self.tokenConsumer.consume(Token.TYPE_RESERVED_WORD)
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             self.Expr()
#             self.tokenConsumer.consume(Token.TYPE_COMMA)
#             self.Type()
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#             return
#         
#         if (self.tokenConsumer.getCurrentType() == Token.TYPE_PAREN_L):
#             self.tokenConsumer.consume(Token.TYPE_PAREN_L)
#             self.Expr()
#             self.tokenConsumer.consume(Token.TYPE_PAREN_R)
#             return
#         
#         try:
#             self.LValue()
#             try:
#                 self.tokenConsumer.consume(Token.TYPE_EQUAL)
#                 self.Expr()
#             except:
#                 pass  
#         except:
#             pass
# 
#     def LValue(self):
#         pass
#         #TODO Impl
        
if __name__ == "__main__":
    with open('../sample1.decaf','r') as f:
        text = f.readlines()
        text = [l.strip() for l in text]
        
    lexer = Lexer(text)
    lexer.evaluate()
    lexer.printTokens()
    
    analyser = SyntacticAnalyser(lexer.tokens)
    analyser.analyse()
    