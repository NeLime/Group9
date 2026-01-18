import ply.yacc as yacc
from rlex import tokens

precedence = (
    ("left", "EQ","NE","GT","LT","GE","LE"),
    ("left", "PLUS","MINUS"),
    ("left", "TIMES","DIVIDE","MOD"),
    ("right", "UMINUS"),
)

def p_program(p):
    "program : stmt_list"
    p[0] = ("program", p[1])

def p_stmt_list(p):
    """stmt_list : stmt_list stmt
                 | stmt"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_stmt(p):
    """stmt : simple_stmt
            | if_stmt
            | while_stmt"""
    p[0] = p[1]

def p_simple_stmt(p):
    """simple_stmt : assign_stmt opt_semi
                   | call_stmt opt_semi"""
    p[0] = p[1]

def p_opt_semi(p):
    """opt_semi : SEMI
                | empty"""
    pass

def p_assign_stmt(p):
    "assign_stmt : ID ASSIGN expr"
    p[0] = ("assign", p[1], p[3])

def p_call_stmt(p):
    """call_stmt : PRINT LPAREN arglist_opt RPAREN
                 | CAT   LPAREN arglist_opt RPAREN"""
    p[0] = ("call", p[1], p[3])

def p_arglist_opt(p):
    """arglist_opt : arglist
                   | empty"""
    p[0] = [] if p[1] is None else p[1]

def p_arglist(p):
    """arglist : arglist COMMA expr
               | expr"""
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

def p_if_stmt(p):
    "if_stmt : IF LPAREN expr RPAREN block else_opt"
    p[0] = ("if", p[3], p[5], p[6])

def p_else_opt(p):
    """else_opt : ELSE block
                | empty"""
    p[0] = None if p[1] is None else p[2]

def p_while_stmt(p):
    "while_stmt : WHILE LPAREN expr RPAREN block"
    p[0] = ("while", p[3], p[5])

def p_block(p):
    "block : LBRACE stmt_list RBRACE"
    p[0] = ("block", p[2])

def p_expr_binop(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MOD expr
            | expr GT expr
            | expr LT expr
            | expr GE expr
            | expr LE expr
            | expr EQ expr
            | expr NE expr"""
    p[0] = ("binop", p[2], p[1], p[3])

def p_expr_uminus(p):
    "expr : MINUS expr %prec UMINUS"
    p[0] = ("uminus", p[2])

def p_expr_group(p):
    "expr : LPAREN expr RPAREN"
    p[0] = p[2]

def p_expr_number(p):
    "expr : NUMBER"
    p[0] = ("num", p[1])

def p_expr_string(p):
    "expr : STRING"
    p[0] = ("str", p[1])

def p_expr_id(p):
    "expr : ID"
    p[0] = ("var", p[1])

def p_empty(p):
    "empty :"
    p[0] = None

def p_error(p):
    if p is None:
        raise SyntaxError("Syntax error: unexpected end of input")
    raise SyntaxError(f"Syntax error at '{p.value}' (type {p.type}) line {getattr(p,'lineno','?')}")

def build_parser(**kwargs):
    return yacc.yacc(**kwargs)
