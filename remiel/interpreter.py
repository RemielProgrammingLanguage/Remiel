# remiel/interpreter.py

from remiel.lexer import RemielLexer
from remiel.parser import Parser
from remiel.executor import Executor

def run_remiel(source_code: str):
    lexer = RemielLexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    executor = Executor()
    executor.execute(ast)

def main():
    with open("main.remiel", "r") as f:
        code = f.read()

    run_remiel(code)

if __name__ == "__main__":
    main()
