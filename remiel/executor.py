# remiel/executor.py

from remiel.parser import Program, ShowCommand, KeepCommand, ReceiveCall, Literal

class RemielExecutor:
    def __init__(self, program: Program):
        self.program = program
        self.env = {}  # variable storage

    def run(self):
        print(f"Running program in mode: {self.program.mode}")
        for stmt in self.program.body:
            self._execute_statement(stmt)

    def _execute_statement(self, stmt):
        if isinstance(stmt, ShowCommand):
            self._execute_show(stmt)
        elif isinstance(stmt, KeepCommand):
            self._execute_keep(stmt)
        else:
            raise RuntimeError(f"Unknown statement type: {type(stmt)}")

    def _execute_show(self, stmt: ShowCommand):
        # stmt.value is string with quotes removed by lexer (if not, strip quotes)
        # Let's strip quotes just in case:
        val = stmt.value.strip('"')
        print(val)

    def _execute_keep(self, stmt: KeepCommand):
        name = stmt.name
        if isinstance(stmt.value, ReceiveCall):
            user_input = input(f"Input value for [{name}]: ")
            self.env[name] = user_input
        elif isinstance(stmt.value, Literal):
            # Handle number or string literals
            val = stmt.value.value
            # convert number strings to int if possible
            if val.isdigit():
                val = int(val)
            elif val.startswith('"') and val.endswith('"'):
                val = val.strip('"')
            self.env[name] = val
        else:
            raise RuntimeError(f"Unsupported value type in keep: {type(stmt.value)}")
