# remiel/lexer.py

import re
from dataclasses import dataclass
from typing import List, Optional

# ----------------------------
# Token Representation
# ----------------------------
@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

# ----------------------------
# Lexer Class
# ----------------------------
class RemielLexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.current = 0
        self.line = 1
        self.column = 1

    def lex(self) -> List[Token]:
        while not self._is_at_end():
            start_column = self.column
            char = self._advance()

            if char in ' \t':
                self.column += 1
                continue
            elif char == '\n':
                self.line += 1
                self.column = 1
                continue
            elif char == '[':
                self._add_token("LBRACKET", '[', start_column)
            elif char == ']':
                self._add_token("RBRACKET", ']', start_column)
            elif char == '=':
                self._add_token("EQUAL", '=', start_column)
            elif char == '(':
                self._add_token("LPAREN", '(', start_column)
            elif char == ')':
                self._add_token("RPAREN", ')', start_column)
            elif char == '"':
                self._lex_string(start_column)
            elif char.isalpha() or char == '_':
                self._lex_identifier_or_keyword(char, start_column)
            elif char.isdigit():
                self._lex_number(char, start_column)
            else:
                self._add_token("UNKNOWN", char, start_column)

        self.tokens.append(Token("EOF", "", self.line, self.column))
        return self.tokens

    def _lex_string(self, start_column):
        value = ''
        while not self._is_at_end() and self._peek() != '"':
            value += self._advance()
        if self._is_at_end():
            raise SyntaxError(f"Unterminated string at line {self.line}")
        self._advance()  # Consume closing quote
        self._add_token("STRING", value, start_column)

    def _lex_identifier_or_keyword(self, first_char, start_column):
        value = first_char
        while not self._is_at_end() and (self._peek().isalnum() or self._peek() == '_'):
            value += self._advance()

        keywords = {
            "strict_mode": "MODE",
            "dynamic_mode": "MODE",
            "universal_mode": "MODE",
            "start": "START",
            "end": "END",
            "show": "SHOW",
            "keep": "KEEP",
            "receive": "RECEIVE"
        }

        token_type = keywords.get(value, "IDENTIFIER")
        self._add_token(token_type, value, start_column)

    def _lex_number(self, first_char, start_column):
        value = first_char
        while not self._is_at_end() and self._peek().isdigit():
            value += self._advance()
        self._add_token("NUMBER", value, start_column)

    def _add_token(self, type_: str, value: str, column: int):
        self.tokens.append(Token(type_, value, self.line, column))

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)
