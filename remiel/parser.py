class ParseError(Exception):
    pass

class RemielParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        token = self.current_token()
        if token is None:
            raise ParseError("Unexpected end of input")
        if expected_type and token.type != expected_type:
            raise ParseError(f"Expected {expected_type} but got {token.type} at line {token.line}")
        self.pos += 1
        return token

    def parse(self):
        self.consume('MODE_DECLARATION')
        self.consume('START')
        while True:
            token = self.current_token()
            if token is None:
                raise ParseError("Missing 'end'")
            if token.type == 'SHOW':
                self.parse_show()
            elif token.type == 'END':
                break
            else:
                raise ParseError(f"Unexpected token {token.type} at line {token.line}")
        self.consume('END')

        if self.current_token() is not None:
            raise ParseError(f"Unexpected code after 'end' at line {self.current_token().line}")

    def parse_show(self):
        self.consume('SHOW')
        self.consume('LBRACKET')
        while self.current_token() and self.current_token().type in ('NUMBER', 'TEXT'):
            self.consume()
        self.consume('RBRACKET')
