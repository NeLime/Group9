from rlex import build_lexer
from rparser import build_parser

class RuntimeErrorR(Exception):
    pass

def lex_tokens(source: str):
    lexer = build_lexer()
    lexer.input(source)
    out = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        out.append({"type": tok.type, "value": tok.value, "line": tok.lineno, "pos": tok.lexpos})
    return out

def parse_ast(source: str):
    lexer = build_lexer()
    parser = build_parser()
    return parser.parse(source, lexer=lexer)

def eval_expr(node, env):
    t = node[0]
    if t == "num": return node[1]
    if t == "str": return node[1]
    if t == "var":
        name = node[1]
        if name not in env:
            raise RuntimeErrorR(f"Undefined variable: {name}")
        return env[name]
    if t == "uminus":
        return -eval_expr(node[1], env)
    if t == "binop":
        op = node[1]
        a = eval_expr(node[2], env)
        b = eval_expr(node[3], env)

        if op == "+":  return a + b
        if op == "-":  return a - b
        if op == "*":  return a * b
        if op == "/":
            if b == 0: raise RuntimeErrorR("Division by zero")
            return a / b
        if op == "%%": return a % b

        if op == ">":  return a > b
        if op == "<":  return a < b
        if op == ">=": return a >= b
        if op == "<=": return a <= b
        if op == "==": return a == b
        if op == "!=": return a != b

        raise RuntimeErrorR(f"Unknown operator: {op}")

    raise RuntimeErrorR(f"Unknown expr node: {t}")

def exec_block(block_node, env, out):
    for st in block_node[1]:
        exec_stmt(st, env, out)

def exec_stmt(node, env, out):
    kind = node[0]

    if kind == "assign":
        _, name, expr = node
        env[name] = eval_expr(expr, env)
        return

    if kind == "call":
        _, fn, args = node
        vals = [eval_expr(a, env) for a in args]

        if fn == "print":
            out.append(" ".join(str(v) for v in vals) + "\n")
            return

        if fn == "cat":
            out.append("".join(str(v) for v in vals))
            return

        raise RuntimeErrorR(f"Unknown function: {fn}")

    if kind == "if":
        _, cond, then_block, else_block = node
        if eval_expr(cond, env):
            exec_block(then_block, env, out)
        elif else_block is not None:
            exec_block(else_block, env, out)
        return

    if kind == "while":
        _, cond, body = node
        guard = 0
        while eval_expr(cond, env):
            exec_block(body, env, out)
            guard += 1
            if guard > 100000:
                raise RuntimeErrorR("Infinite loop suspected (guard limit reached)")
        return

    raise RuntimeErrorR(f"Unknown stmt node: {kind}")

def run_all(source: str):
    try:
        tokens = lex_tokens(source)
        ast = parse_ast(source)

        env = {}
        out = []
        for st in ast[1]:
            exec_stmt(st, env, out)

        return {"ok": True, "tokens": tokens, "ast": ast, "output": "".join(out), "error": ""}
    except Exception as e:
        return {"ok": False, "tokens": [], "ast": None, "output": "", "error": str(e)}
