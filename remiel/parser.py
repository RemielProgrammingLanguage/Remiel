# remiel/parser.py

from remiel.token_type import TokenType
from remiel.token import Token

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []

        while not self.is_at_end():
            stmt = self.statement()
            if stmt:
                statements.append(stmt)

        return statements
    # ------------------------
    #Mode Declaration
    #------------------------
    def mode_declaration(self):
     tok = self.advance()  # Consume the mode token (MODE_STRICT, etc.)
     return {"type": "ModeDeclaration", "mode": tok.type.name}
    # ------------------------
    # Statement Parsing
    # ------------------------
    def statement(self):
     tok = self.peek()

     if tok.type in (TokenType.MODE_STRICT, TokenType.MODE_DYNAMIC, TokenType.MODE_UNIVERSAL):
         return self.mode_declaration()
     elif tok.type == TokenType.START:
         return self.program_block()
     elif tok.type == TokenType.SHOW:
         return self.show_statement()
     elif tok.type == TokenType.KEEP:
         return self.keep_statement()
     elif self.check(TokenType.RECEIVE):
          value = self.parse_receive()
     elif tok.type in (TokenType.TYPE_NATURAL, TokenType.TYPE_POINT, TokenType.TYPE_TEXT, TokenType.TYPE_FLIP):
         return self.typed_keep_statement()  
     elif tok.type in (TokenType.COMMENT_SINGLE, TokenType.COMMENT_MULTI_START):
         self.skip_comment()
         return None
     elif tok.type == TokenType.EXPLAIN:
         return self.explain_comment()
     else:
         self.error(tok, f"Unexpected token: {tok.type}")
         return None
    def program_block(self):
     self.consume(TokenType.START, "Expected 'start'")
     body = []

     while not self.check(TokenType.END) and not self.is_at_end():
         stmt = self.statement()
         if stmt:
             body.append(stmt)

     self.consume(TokenType.END, "Expected 'end'")
     return {
         "type": "block",
         "statements": body
     }
    def show_statement(self):
     self.consume(TokenType.SHOW, "Expected 'show'")
     self.consume(TokenType.LBRACKET, "Expected '[' after 'show'")

     expr_tokens = []  # Initialize the list to collect tokens

     # Collect tokens until we reach the closing bracket or end of input
     while not self.check(TokenType.RBRACKET) and not self.is_at_end():
         expr_tokens.append(self.advance())

     self.consume(TokenType.RBRACKET, "Expected ']' after show expression")

     return {
         "type": "show",
         "expression": expr_tokens
     }
    def typed_keep_statement(self):
     # Consume the type first
     type_token = self.advance()

     # Now expect `keep`
     self.consume(TokenType.KEEP, "Expected 'keep' after type declaration")

     self.consume(TokenType.LBRACKET, "Expected '[' before variable name")

     identifier = self.consume(TokenType.IDENTIFIER, "Expected variable name")

     self.consume(TokenType.RBRACKET, "Expected ']' after variable name")

     self.consume(TokenType.ASSIGN, "Expected '=' after variable name")

     # Now determine value by type
     if type_token.type == TokenType.TYPE_NATURAL:
         value_token = self.consume(TokenType.NATURAL_LITERAL, "Expected natural literal")
     elif type_token.type == TokenType.TYPE_POINT:
         value_token = self.consume(TokenType.POINT_LITERAL, "Expected point literal")
     elif type_token.type == TokenType.TYPE_TEXT:
         value_token = self.consume(TokenType.TEXT_LITERAL, "Expected text literal")
     elif type_token.type == TokenType.TYPE_FLIP:
         value_token = self.consume(TokenType.BOOLEAN_LITERAL, "Expected flip literal")
     else:
         raise self.error(type_token, f"Unknown type: {type_token.type}")

     # Return some AST node (simplified)
     return {
         "type": "typed_keep",
         "datatype": type_token.type,
         "name": identifier.value,
         "value": value_token.value
     }
    def keep_statement(self):
     self.consume(TokenType.KEEP, "Expected 'keep' keyword")

     self.consume(TokenType.LBRACKET, "Expected '[' before variable name")
     identifier = self.consume(TokenType.IDENTIFIER, "Expected variable name")
     self.consume(TokenType.RBRACKET, "Expected ']' after variable name")

     self.consume(TokenType.ASSIGN, "Expected '=' after variable name")

     # Now determine what kind of value follows (literal or expression)
     value_token = self.peek()

     if value_token.type in (
         TokenType.NATURAL_LITERAL,
         TokenType.POINT_LITERAL,
         TokenType.TEXT_LITERAL,
         TokenType.BOOLEAN_LITERAL,
         TokenType.IDENTIFIER,
     ):
         value = self.advance()
     elif value_token.type == TokenType.RECEIVE:
         value = self.parse_receive()
     else:
         self.error(value_token, f"Unexpected value in 'keep' assignment")

     return {
      "type": "keep",
      "name": identifier.value,
      "value": value.value if isinstance(value, Token) else value,
      "value_type": value.type if isinstance(value, Token) else None
     }
    #________________
    #Parse
    #________________
    def parse_receive(self):
        # Parses: receive()
        self.consume(TokenType.RECEIVE, "Expected 'receive' keyword")
        self.consume(TokenType.LPAREN, "Expected '(' after 'receive'")
        self.consume(TokenType.RPAREN, "Expected ')' after '(' in receive")

        return {
            "type": "receive_call"
        }
    # ------------------------
    # Expressions
    # ------------------------
    def expression(self):
        if self.match(TokenType.MATH):
            return self.math_expr()
        return self.advance()

    def math_expr(self):
        self.consume(TokenType.MATH, "Expected 'math'")
        self.consume(TokenType.LEFT_BRACE, "Expected '{'")
        expr_tokens = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            expr_tokens.append(self.advance())

        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after math expression")
        return ("math", expr_tokens)

    # ------------------------
    # Utilities
    # ------------------------
    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()
        self.error(self.peek(), message)

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def error(self, token, message):
    # Try to get line info
     if hasattr(token, 'pos'):
         line = token.pos[0]
     elif hasattr(token, 'line'):
         line = token.line
     else:
         line = "unknown"
     raise ParserError(f"[Line {line}] Error at '{token.value}': {message}")
   #############
   #Skip Comment
   #############
    def skip_comment(self):
     tok = self.advance()

     # If it's a single-line comment, just skip
     if tok.type == TokenType.COMMENT_SINGLE:
         return

     # If it's a multi-line comment, skip until the end marker
     if tok.type == TokenType.COMMENT_MULTI_START:
         while not self.match(TokenType.COMMENT_MULTI_END):
             if self.is_at_end():
                 self.error(tok, "Unterminated multi-line comment")
                 break
             self.advance()
