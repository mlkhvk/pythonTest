"""Модуль калькулятора: 
преобразование инфиксной записи в обратную польскую и вычисление выражений."""

def infix_to_rpn(expression):
    """Преобразует инфиксное выражение в обратную польскую запись (ОПЗ)."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    tokens = tokenize(expression)
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.isnumeric() or is_float(token):
            output.append(token)
        elif token in precedence:
            # Обработка унарных + и -
            if (token in ('+', '-') and 
                (i == 0 or tokens[i-1] == '(' or tokens[i-1] in precedence)):
                # Это унарный оператор
                if token == '-':
                    output.append('0')  # Добавляем 0 для унарного минуса
                # Унарный плюс просто игнорируем
            else:
                # Это бинарный оператор
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
        i += 1

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
            if token in ('+', '-', '*', '/', '^'):
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов")
                operand_b = stack.pop()
                operand_a = stack.pop()
                if token == '+':
                    stack.append(operand_a + operand_b)
                elif token == '-':
                    stack.append(operand_a - operand_b)
                elif token == '*':
                    stack.append(operand_a * operand_b)
                elif token == '/':
                    if operand_b == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    stack.append(operand_a / operand_b)
                elif token == '^':
                    stack.append(operand_a ** operand_b)
            else:
                raise ValueError(f"Неизвестный оператор: {token}")
    
    if len(stack) != 1:
        raise ValueError("После вычисления остались лишние операнды")
    return stack[0]


def tokenize(expression):
    """Разбивает строку выражения на числа, операторы и скобки."""
    tokens = []
    number = ''
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        if char.isdigit() or char == '.':
            number += char
        else:
            if number:
                tokens.append(number)
                number = ''
            
            if char in '+-*/^()':
                # Обработка унарных операторов
                if char in ('+', '-'):
                    if (i == 0 or expression[i-1] == '(' or 
                        expression[i-1] in '+-*/^'):
                        # Это унарный оператор
                        tokens.append(char)
                    else:
                        # Это бинарный оператор
                        tokens.append(char)
                else:
                    tokens.append(char)
            elif char.isspace():
                pass  # Игнорируем пробелы
            else:
                raise ValueError(f"Недопустимый символ: {char}")
        i += 1
    
    if number:
        tokens.append(number)
    
    return tokens


def is_float(string):
    """Проверяет, является ли строка числом с плавающей точкой."""
    try:
        float(string)
        return True
    except ValueError:
        return False


def main():
    """Основная функция для запуска калькулятора."""
    expr = input("Введите выражение: ")
    rpn = infix_to_rpn(expr)
    print("ОПЗ:", " ".join(rpn))
    print("Результат:", evaluate_rpn(rpn))


if __name__ == "__main__":
    main()