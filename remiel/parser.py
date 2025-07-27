# remiel/parser.py

from remiel.lexer import RemielLexer, Token
from typing import List

# ----------------------------
# AST Node Definitions
# ----------------------------

class ASTNode: pass

class Program(ASTNode):
    def __init__(self, mode: str, body: List[ASTNode]):
        self.mode = mode
        self.body = body

class ShowCommand(ASTNode):
    def __init__(self, value: str):
        self.value = value

class KeepCommand(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

class ReceiveCall(ASTNode): pass

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

# ----------------------------
# Parser Class
# ----------------------------

class RemielParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        mode_token = self._consume("MODE", "Expected mode declaration (strict_mode, etc)")
        self._consume("START", "Expected 'start'")
        body = []

        while not self._check("END") and not self._is_at_end():
            body.append(self._parse_statement())

        self._consume("END", "Expected 'end'")
        return Program(mode_token.value, body)

    def _parse_statement(self) -> ASTNode:
        if self._match("SHOW"):
            self._consume("LBRACKET", "Expected '[' after 'show'")
            string_token = self._consume("STRING", "Expected string inside show")
            self._consume("RBRACKET", "Expected ']' after string")
            return ShowCommand(string_token.value)

        elif self._match("KEEP"):
            self._consume("LBRACKET", "Expected '[' after 'keep'")
            name_token = self._consume("IDENTIFIER", "Expected variable name")
            self._consume("RBRACKET", "Expected ']' after variable name")
            self._consume("EQUAL", "Expected '='")

            if self._match("RECEIVE"):
                self._consume("LPAREN", "Expected '(' after receive")
                self._consume("RPAREN", "Expected ')'")
                return KeepCommand(name_token.value, ReceiveCall())

            elif self._check("NUMBER") or self._check("STRING"):
                value_token = self._advance()
                return KeepCommand(name_token.value, Literal(value_token.value))

            else:
                raise SyntaxError(f"Invalid value after keep at line {self._peek().line}")

        else:
            raise SyntaxError(f"Unexpected token '{self._peek().value}' at line {self._peek().line}")

    # ----------------------------
    # Helpers
    # ----------------------------

    def _match(self, *types):
        if self._check(*types):
            self._advance()
            return True
        return False

    def _check(self, *types):
        if self._is_at_end():
            return False
        return self._peek().type in types

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _consume(self, type_, message):
        if self._check(type_):
            return self._advance()
        raise SyntaxError(message + f" at line {self._peek().line}")

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _is_at_end(self):
        return self._peek().type == "EOF"
