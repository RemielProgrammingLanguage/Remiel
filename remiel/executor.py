class RemielExecutor:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        token = self.current_token()
        if token is None:
            raise RuntimeError("Unexpected end of input during execution")
        if expected_type and token.type != expected_type:
            raise RuntimeError(f"Expected {expected_type} but got {token.type} at line {token.line}")
        self.pos += 1
        return token

    def execute(self):
        self.consume('MODE_DECLARATION')
        self.consume('START')
        while True:
            token = self.current_token()
            if token is None:
                raise RuntimeError("Missing 'end' keyword")
            if token.type == 'SHOW':
                self.execute_show()
            elif token.type == 'END':
                self.consume('END')
                break
            else:
                raise RuntimeError(f"Invalid token {token.type} at line {token.line}")

    def execute_show(self):
        self.consume('SHOW')
        self.consume('LBRACKET')
        contents = []
        while self.current_token() and self.current_token().type in ('NUMBER', 'TEXT'):
            contents.append(self.consume().value)
        self.consume('RBRACKET')
        print(" ".join(contents))
