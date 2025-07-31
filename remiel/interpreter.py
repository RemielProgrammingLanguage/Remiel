from remiel.lexer import RemielLexer
from remiel.parser import RemielParser, ParseError
from remiel.executor import RemielExecutor

class RemielInterpreter:
    def __init__(self, source_code):
        self.source_code = source_code

    def run(self):
        try:
            # Tokenize
            lexer = RemielLexer(self.source_code)
            tokens = lexer.tokenize()

            # Parse
            parser = RemielParser(tokens)
            parser.parse()

            # Execute
            executor = RemielExecutor(tokens)
            executor.execute()

        except (ParseError, RuntimeError) as e:
            print("Error:", e)
