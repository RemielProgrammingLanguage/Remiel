import re

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, line={self.line}, col={self.column})'

class RemielLexer:
    token_specification = [
        ('MODE_DECLARATION', r'strict_mode|dynamic_mode|universal_mode'),
        ('START',            r'start'),
        ('END',              r'end'),
        ('SHOW',             r'show'),
        ('LBRACKET',         r'\['),
        ('RBRACKET',         r'\]'),
        ('NUMBER',           r'\d+'),
        ('TEXT',             r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NEWLINE',          r'\n'),
        ('SKIP',             r'[ \t]+'),
        ('MISMATCH',         r'.'),
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line_num = 1
        self.line_start = 0
        self.mode_declared = False

        parts = [f'(?P<{name}>{pattern})' for name, pattern in self.token_specification]
        self.regex = re.compile('|'.join(parts))

    def tokenize(self):
        for mo in self.regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - self.line_start + 1

            if kind == 'NEWLINE':
                self.line_num += 1
                self.line_start = mo.end()
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Illegal character {value!r} at line {self.line_num} column {column}')
            elif kind == 'MODE_DECLARATION':
                if self.mode_declared:
                    raise RuntimeError(f'Mode already declared at line {self.line_num}')
                self.mode_declared = True
                self.tokens.append(Token(kind, value, self.line_num, column))
            else:
                self.tokens.append(Token(kind, value, self.line_num, column))

        return self.tokens
