import re

class Err(Exception):
    pass

def empty(s):
    if s.strip() == "":
        raise Err("Ошибка: пустой ввод")

def chars(s):
    if re.search(r"[^0-9.+\-*/<(),\s]", s.replace("pow", "")):
        raise Err("Ошибка: некорректные символы в выражении")

def brackets(s):
    b = 0
    for c in s:
        if c == "(":
            b += 1
        elif c == ")":
            b -= 1
            if b < 0:
                raise Err("Ошибка: несогласованное количество скобок")
    if b > 0:
        raise Err("Ошибка: отсутствует закрывающая скобка")


def lex(s):
    return re.findall(r"\d+\.?\d*|\.\d+|pow|[+\-*/<(),]|\S", s)

t = []
i = 0

def cur():
    if i < len(t):
        return t[i]
    return None

def eat(x):
    global i
    if cur() != x:
        if x == ")" and cur() is None:
            raise Err("Ошибка: отсутствует закрывающая скобка")
        raise Err("Ошибка: некорректное арифметическое выражение")
    i += 1

def expr():
    global i
    r = add()
    if cur() == "<":
        i += 1
        n = add()
        r = r < n
        if cur() == "<":
            raise Err("Ошибка: допускается только один оператор сравнения '<'")
    return r

def add():
    global i
    r = mul()
    while cur() in ("+", "-"):
        op = cur()
        i += 1
        n = mul()
        if op == "+":
            r = r + n
        else:
            r = r - n
    return r

def mul():
    global i
    r = un()
    while cur() in ("*", "/"):
        op = cur()
        i += 1
        n = un()
        if op == "*":
            r = r * n
        else:
            if n == 0:
                raise Err("Ошибка: деление на ноль")
            r = r / n
    return r

def un():
    global i
    if cur() == "-":
        i += 1
        return -un()
    if cur() == "+":
        i += 1
        return un()
    return prim()

def prim():
    global i
    c = cur()
    if c is None:
        raise Err("Ошибка: некорректное арифметическое выражение")
    if re.fullmatch(r"\d+\.?\d*|\.\d+", c):
        i += 1
        if "." in c:
            return float(c)
        return int(c)
    if c == "(":
        i += 1
        r = expr()
        eat(")")
        return r
    if c == "pow":
        i += 1
        eat("(")
        a = expr()
        eat(",")
        b = expr()
        eat(")")
        return pw(a, b)
    raise Err("Ошибка: некорректное арифметическое выражение")

def pw(a, b):
    if a == 0 and b < 0:
        raise Err("Ошибка: деление на ноль (0 в отрицательной степени)")
    r = a ** b
    if isinstance(r, complex):
        raise Err("Ошибка: результат pow не является вещественным числом")
    return r


def calc(s):
    global t, i
    empty(s)
    chars(s)
    brackets(s)
    t = lex(s)
    i = 0
    try:
        r = expr()
    except OverflowError:
        raise Err("Ошибка: слишком большое число")
    if i != len(t):
        raise Err("Ошибка: некорректное арифметическое выражение")
    return r


print("Введите выражение или 'exit' для выхода")
while True:
    s = input(">>> ")
    if s.strip().lower() == "exit":
        break
    try:
        r = calc(s)
        if r is True:
            print("Правда")
        elif r is False:
            print("Ложь")
        else:
            print(r)
    except Err as e:
        print(e)
