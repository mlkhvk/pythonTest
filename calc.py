"""Модуль калькулятора: 
преобразование инфиксной записи в 
обратную польскую и вычисление выражений."""

def infix_to_rpn(expression):
    """Преобразует инфиксное выражение 
    в обратную польскую запись (ОПЗ)."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []
    tokens = tokenize(expression)

    for token in tokens:
        if token.isnumeric() or is_float(token):
            output.append(token)
        elif token in precedence:
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Пропущена открывающая скобка")
            stack.pop()
        else:
            raise ValueError(f"Неизвестный токен: {token}")

    while stack:
        if stack[-1] in ('(', ')'):
            raise ValueError("Непарные скобки в выражении")
        output.append(stack.pop())

    return output


def evaluate_rpn(tokens):
    """Вычисляет выражение в обратной польской записи (ОПЗ)."""
    stack = []
    for token in tokens:
        if token.isnumeric() or is_float(token):
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                stack.append(a / b)
            else:
                raise ValueError(f"Неизвестный оператор: {token}")
    if len(stack) != 1:
        raise ValueError("После вычисления остались лишние операнды")
    return stack[0]


def tokenize(expression):
    """Разбивает строку выражения на числа, операторы и скобки."""
    tokens = []
    number = ''
    for ch in expression:
        if ch.isdigit() or ch == '.':
            number += ch
        else:
            if number:
                tokens.append(number)
                number = ''
            if ch in '+-*/()':
                tokens.append(ch)
            elif ch.isspace():
                continue
            else:
                raise ValueError(f"Недопустимый символ: {ch}")
    if number:
        tokens.append(number)
    return tokens


def is_float(s):
    """Проверяет, является ли строка числом с плавающей точкой."""
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    expr = input("Введите выражение: ")
    rpn = infix_to_rpn(expr)
    print("ОПЗ:", " ".join(rpn))
    print("Результат:", evaluate_rpn(rpn))
