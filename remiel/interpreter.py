import sys
from remiel.lexer import RemielLexer
from remiel.parser import RemielParser, ShowCommand, KeepCommand, ReceiveCall
from remiel.executor import RemielExecutor

def run_remiel_code(filepath):
    with open(filepath, 'r') as file:
        source = file.read()

    print("[Remiel v0.1] Lexing...")
    lexer = RemielLexer(source)
    tokens = lexer.lex()

    print("[Remiel v0.1] Parsing...")
    parser = RemielParser(tokens)
    program = parser.parse()

    print("[Remiel v0.1] Executing...")
    executor = RemielExecutor(program)
    executor.run()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 interpreter.py <filename>")
    else:
        run_remiel_code(sys.argv[1])
