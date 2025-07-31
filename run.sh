#!/data/data/com.termux/files/usr/bin/bash
echo "Running Remiel program..."
python3 -u -c "
from remiel.interpreter import RemielInterpreter
with open('main.remiel') as f:
    code = f.read()
RemielInterpreter(code).run()
"
