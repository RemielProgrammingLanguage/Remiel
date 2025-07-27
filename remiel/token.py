# remiel/token.py

class Token:
    def __init__(self, type_, value=None, position=None):
        """
        Represents a token produced by the lexer.

        Args:
            type_ (TokenType): The type of the token (from TokenType enum).
            value (optional): The literal value of the token (e.g., number, string, identifier name).
            position (optional): Position in the source code as a string, e.g., "line:column".
        """
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, pos={self.position})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and
                self.value == other.value and
                self.position == other.position)
