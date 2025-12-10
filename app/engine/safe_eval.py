import ast

class SafeEvaluator(ast.NodeVisitor):
    allowed_nodes = (
        ast.Expression, ast.BoolOp, ast.Compare, ast.Name, ast.Load,
        ast.Constant, ast.And, ast.Or, ast.Gt, ast.Lt, ast.GtE, ast.LtE,
        ast.Eq, ast.NotEq, ast.Subscript, ast.Index
    )

    def __init__(self, state):
        self.state = state

    def visit(self, node):
        if not isinstance(node, self.allowed_nodes):
            raise ValueError(f"Unsafe expression: {type(node).__name__}")
        return super().visit(node)

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        if node.id == "state":
            return self.state
        raise ValueError("Only 'state' may be referenced")

    def visit_Subscript(self, node):
        target = self.visit(node.value)
        key = self.visit(node.slice)
        return target[key]

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        op = node.ops[0]
        if isinstance(op, ast.Lt):
            return left < right
        if isinstance(op, ast.Gt):
            return left > right
        if isinstance(op, ast.Eq):
            return left == right
        if isinstance(op, ast.NotEq):
            return left != right
        if isinstance(op, ast.GtE):
            return left >= right
        if isinstance(op, ast.LtE):
            return left <= right
        raise ValueError("Unsupported operator")

    def visit_BoolOp(self, node):
        if isinstance(node.op, ast.And):
            return all(self.visit(v) for v in node.values)
        if isinstance(node.op, ast.Or):
            return any(self.visit(v) for v in node.values)
        raise ValueError("Unsupported boolean operator")


def safe_eval(expr: str, state: dict):
    try:
        tree = ast.parse(expr, mode="eval")
        evaluator = SafeEvaluator(state)
        return evaluator.visit(tree)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expr}. Error: {e}")
