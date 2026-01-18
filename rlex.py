import ply.lex as lex

reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "print": "PRINT",
    "cat": "CAT",
}

tokens = [
    "ID", "NUMBER", "STRING",
    "ASSIGN",                # <-
    "PLUS","MINUS","TIMES","DIVIDE",
    "LPAREN","RPAREN",
    "LBRACE","RBRACE",
    "COMMA","SEMI",
    "GT","LT","GE","LE","EQ","NE",
    "MOD",                   # %%
] + list(reserved.values())

t_ASSIGN = r"<-"
t_MOD = r"%%"

t_PLUS   = r"\+"
t_MINUS  = r"-"
t_TIMES  = r"\*"
t_DIVIDE = r"/"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA  = r","
t_SEMI   = r";"

t_GE = r">="
t_LE = r"<="
t_EQ = r"=="
t_NE = r"!="
t_GT = r">"
t_LT = r"<"

t_ignore = " \t"

def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t

def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r"\#.*"
    pass

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

def build_lexer(**kwargs):
    return lex.lex(**kwargs)
