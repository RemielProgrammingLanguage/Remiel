# remiel/token_type.py
from enum import Enum

class TokenType(Enum):
    # Modes
    MODE_STRICT = 'MODE_STRICT'
    MODE_DYNAMIC = 'MODE_DYNAMIC'
    MODE_UNIVERSAL = 'MODE_UNIVERSAL'

    # Program structure
    START = 'START'
    END = 'END'

    # Keywords (statements)
    SHOW = 'SHOW'
    KEEP = 'KEEP'
    RECEIVE = 'RECEIVE'
    MATH = 'MATH'

    # Primitive Types
    TYPE_NATURAL = 'TYPE_NATURAL'
    TYPE_POINT = 'TYPE_POINT'
    TYPE_TEXT = 'TYPE_TEXT'
    TYPE_FLIP = 'TYPE_FLIP'

    # Literals
    NATURAL_LITERAL = 'NATURAL_LITERAL'      # e.g., 123
    POINT_LITERAL = 'POINT_LITERAL'          # e.g., 3.14
    TEXT_LITERAL = 'TEXT_LITERAL'            # e.g., "hello"
    BOOLEAN_LITERAL = 'BOOLEAN_LITERAL'      # true/false

    # Identifiers
    IDENTIFIER = 'IDENTIFIER'                 # variable names, function names

    # Operators & Symbols
    ASSIGN = 'ASSIGN'                        # =
    LBRACKET = 'LBRACKET'                    # [
    RBRACKET = 'RBRACKET'                    # ]
    LBRACE = 'LBRACE'                        # {
    RBRACE = 'RBRACE'                        # }
    LPAREN = 'LPAREN'                        # (
    RPAREN = 'RPAREN'                        # )
    COMMA = 'COMMA'                          # ,
    PLUS = 'PLUS'                            # +
    MINUS = 'MINUS'                          # -
    MUL = 'MUL'                              # *
    DIV = 'DIV'                              # /
    MOD = 'MOD'                              # %
    POW = 'POW'                              # ^

    # Comments
    COMMENT_SINGLE = 'COMMENT_SINGLE'        # note:
    COMMENT_MULTI_START = 'COMMENT_MULTI_START'  # explain:!
    COMMENT_MULTI_END = 'COMMENT_MULTI_END'      # !

    # End of file
    EOF = 'EOF'
