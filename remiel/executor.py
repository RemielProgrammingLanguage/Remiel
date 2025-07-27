# remiel/executor.py

class Executor:
    def __init__(self):
        # Store variables here
        self.variables = {}

    def execute(self, node):
        if isinstance(node, list):
            # Execute a list of nodes (statements)
            for stmt in node:
                self.execute(stmt)
            return

        if not isinstance(node, dict):
            raise Exception(f"Invalid AST node: {node}")

        node_type = node.get("type")

        if node_type == "block":
            for stmt in node.get("statements", []):
                self.execute(stmt)

        elif node_type == "ModeDeclaration":
            # For now just print or store mode info
            print(f"[Mode] Mode declared: {node['mode']}")

        elif node_type == "typed_keep":
            var_name = node["name"]
            value = node["value"]
            # You can add type checks here if you want
            self.variables[var_name] = value
            print(f"[Variable] {var_name} (typed) = {value}")

        elif node_type == "keep":
            var_name = node["name"]
            value_node = node["value"]

            # Support receive call (input)
            if isinstance(value_node, dict) and value_node.get("type") == "receive_call":
                user_input = input(f"Input for {var_name}: ")
                self.variables[var_name] = user_input
                print(f"[Variable] {var_name} (received input) = {user_input}")
            else:
                # Otherwise assign direct value
                self.variables[var_name] = value_node
                print(f"[Variable] {var_name} = {value_node}")

        elif node_type == "show":
            # node["expressions"] is a list of tokens or AST nodes (depending on your parser)
            # For now, we simply print literals or variables if matched
            output_parts = []
            for expr in node.get("expressions", []):
                # If expr is a Token or dict, you may need to handle accordingly
                # For demo, assume expr is either:
                # - Token with type IDENTIFIER: look up variable
                # - Literal value (int, float, str)
                if isinstance(expr, str):
                    output_parts.append(expr)
                elif isinstance(expr, dict):
                    # Nested expression, not implemented here
                    output_parts.append(str(expr))
                else:
                    # Could be a token with type and value
                    try:
                        val = self._eval_expr(expr)
                        output_parts.append(str(val))
                    except Exception:
                        output_parts.append(str(expr))
            print("[Output]", " ".join(output_parts))

        else:
            raise Exception(f"Unknown node type: {node_type}")

    def _eval_expr(self, token):
        # Simplified eval for expressions (could expand later)
        # If token is a variable identifier, return variable value
        # If token is literal, return its value

        # token expected to be a Token object or dict or literal

        if hasattr(token, "type"):
            # Token object with .type and .value
            if token.type.name == "IDENTIFIER":
                return self.variables.get(token.value, f"<undefined {token.value}>")
            else:
                return token.value
        elif isinstance(token, dict):
            # Could be nested AST expr
            # Not implemented yet
            return str(token)
        else:
            # Plain literal
            return token
