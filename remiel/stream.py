# remiel/stream.py

class CharStream:
    def __init__(self, source):
        """
        Initializes the character stream.

        Args:
            source (str): The full source code as a string.
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def peek(self, ahead=0):
        """
        Peek at the current or future character without consuming it.

        Args:
            ahead (int): Number of characters to look ahead.
        Returns:
            str: The character at the current + ahead position or '\0' at EOF.
        """
        if self.pos + ahead >= len(self.source):
            return '\0'  # Null char to represent EOF
        return self.source[self.pos + ahead]

    def advance(self):
        """
        Advance to the next character, updating line/column info.

        Returns:
            str: The character just consumed.
        """
        char = self.peek()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return char

    def position(self):
        """
        Returns the current position in the source for debugging/error reporting.

        Returns:
            str: A string in the format 'line:column'.
        """
        return f"{self.line}:{self.col}"
