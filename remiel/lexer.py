# remiel/lexer.py

from remiel.token_type import TokenType
from remiel.token import Token
from remiel.stream import CharStream

class RemielLexer:
    def __init__(self, source):
        self.stream = CharStream(source)
        self.tokens = []
        self.in_multiline_comment = False

        self.keywords = {
            'strict_mode': TokenType.MODE_STRICT,
            'dynamic_mode': TokenType.MODE_DYNAMIC,
            'universal_mode': TokenType.MODE_UNIVERSAL,

            'start': TokenType.START,
            'end': TokenType.END,

            'show': TokenType.SHOW,
            'keep': TokenType.KEEP,
            'receive': TokenType.RECEIVE,
            'math': TokenType.MATH,

            'natural': TokenType.TYPE_NATURAL,
            'point': TokenType.TYPE_POINT,
            'text': TokenType.TYPE_TEXT,
            'flip': TokenType.TYPE_FLIP,

            'true': TokenType.BOOLEAN_LITERAL,
            'false': TokenType.BOOLEAN_LITERAL,
        }

        self.symbols = {
            '=': TokenType.ASSIGN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MUL,
            '/': TokenType.DIV,
            '%': TokenType.MOD,
            '^': TokenType.POW,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
        }

    def tokenize(self):
        while True:
            self._skip_whitespace()
            pos = self.stream.position()
            char = self.stream.peek()

            if char == '\0':
                self.tokens.append(Token(TokenType.EOF, None, pos))
                break

            if self.in_multiline_comment:
                if self._check("!"):
                    self.stream.advance()
                    self.tokens.append(Token(TokenType.COMMENT_MULTI_END, "!", pos))
                    self.in_multiline_comment = False
                else:
                    self.stream.advance()
                continue

            if self._check("note:"):
                self._consume_line_comment()
                continue
            if self._check("explain:!"):
                self._consume_multiline_comment_start()
                continue
            elif char == '"':
                self.tokens.append(self._string())
            elif char.isdigit():
                self.tokens.append(self._number())
            elif char.isalpha() or char == '_':
                self.tokens.append(self._identifier_or_keyword())
            elif char in self.symbols:
                self.tokens.append(self._symbol())
            else:
                raise Exception(f"Unknown character '{char}' at {pos}")

        return self.tokens

    def _check(self, string):
        for i in range(len(string)):
            if self.stream.peek(i) != string[i]:
                return False
        return True

    def _skip_whitespace(self):
        while self.stream.peek().isspace():
            self.stream.advance()

    def _consume_line_comment(self):
        pos = self.stream.position()
        content = ""
        while self.stream.peek() != '\n' and self.stream.peek() != '\0':
            content += self.stream.advance()
        self.tokens.append(Token(TokenType.COMMENT_SINGLE, content, pos))

    def _consume_multiline_comment_start(self):
        pos = self.stream.position()
        self.stream.advance()  # e
        self.stream.advance()  # x
        self.stream.advance()  # p
        self.stream.advance()  # l
        self.stream.advance()  # a
        self.stream.advance()  # i
        self.stream.advance()  # n
        self.stream.advance()  # :
        self.stream.advance()  # !
        self.tokens.append(Token(TokenType.COMMENT_MULTI_START, "explain:!", pos))
        self.in_multiline_comment = True

    def _string(self):
        pos = self.stream.position()
        self.stream.advance()  # skip opening "
        value = ""
        while self.stream.peek() != '"' and self.stream.peek() != '\0':
            value += self.stream.advance()
        if self.stream.peek() != '"':
            raise Exception(f"Unclosed string at {pos}")
        self.stream.advance()  # skip closing "
        return Token(TokenType.TEXT_LITERAL, value, pos)

    def _number(self):
        pos = self.stream.position()
        value = ""
        is_float = False
        while self.stream.peek().isdigit() or self.stream.peek() == '.':
            if self.stream.peek() == '.':
                if is_float:
                    break
                is_float = True
            value += self.stream.advance()

        return Token(
            TokenType.POINT_LITERAL if is_float else TokenType.NATURAL_LITERAL,
            float(value) if is_float else int(value),
            pos
        )

    def _identifier_or_keyword(self):
        pos = self.stream.position()
        ident = ""
        while self.stream.peek().isalnum() or self.stream.peek() == '_':
            ident += self.stream.advance()

        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        value = ident if token_type == TokenType.IDENTIFIER else None
        return Token(token_type, value, pos)

    def _symbol(self):
        pos = self.stream.position()
        char = self.stream.advance()
        token_type = self.symbols.get(char)
        return Token(token_type, char, pos)
