"""Модуль тестов для калькулятора."""

from calc import infix_to_rpn, evaluate_rpn

def test_calculator_functions():
    """Выполняет все тесты калькулятора."""
    tests = [
        (
            "3 + 4 * 2",
         ["3", "4", "2", "*", "+"],
         11.0
        ),
        (
            "(3 + 4) * 2",
         ["3", "4", "+", "2", "*"],
         14.0
        ),
        (
            "10 + 2 * 6",
         ["10", "2", "6", "*", "+"],
         22.0
        ),
        (
            "100 * 2 + 12",
         ["100", "2", "*", "12", "+"],
         212.0
        ),
        (
            "100 * ( 2 + 12 )",
         ["100", "2", "12", "+", "*"],
         1400.0
        ),
        (
            "100 * ( 2 + 12 ) / 14",
         ["100", "2", "12", "+", "*", "14", "/"],
         100.0
        )
    ]

    for expr, expected_rpn, expected_result in tests:
        rpn = infix_to_rpn(expr)
        assert rpn == expected_rpn, f"Ожидалось {expected_rpn}, получено {rpn}"
        result = evaluate_rpn(rpn)
        assert abs(result - expected_result) < 1e-9, f"Ожидалось {expected_result}, получено {result}"

if __name__ == "__main__":
    test_calculator_functions()
    print("Все тесты пройдены!")
