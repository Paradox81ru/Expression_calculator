import pytest

from expression_calculator.calculator import Calculator
from expression_calculator.parser_expression import ParserExpression


def test_parse_expression():
    """ Тестирует разбор строки на лексемы """
    expr = "12+ (23+5*4/(12-6)+37)+ 45 -(43-56*1274-(72+9))"
    expected_result = [
        ('NUMBER', 12),
        ('SIGN', '+'),
        ('PARENTHESIS', 1),
        ('NUMBER', 23),
        ('SIGN', '+'),
        ('NUMBER', 5),
        ('SIGN', '*'),
        ('NUMBER', 4),
        ('SIGN', '/'),
        ('PARENTHESIS', 2),
        ('NUMBER', 12),
        ('SIGN', '-'),
        ('NUMBER', 6),
        ('PARENTHESIS_CLOSE', 2),
        ('SIGN', '+'),
        ('NUMBER', 37),
        ('PARENTHESIS_CLOSE', 1),
        ('SIGN', '+'),
        ('NUMBER', 45),
        ('SIGN', '-'),
        ('PARENTHESIS', 1),
        ('NUMBER', 43),
        ('SIGN', '-'),
        ('NUMBER', 56),
        ('SIGN', '*'),
        ('NUMBER', 1274),
        ('SIGN', '-'),
        ('PARENTHESIS', 2),
        ('NUMBER', 72),
        ('SIGN', '+'),
        ('NUMBER', 9),
        ('PARENTHESIS_CLOSE', 2),
        ('PARENTHESIS_CLOSE', 1)
    ]

    parse_expression = ParserExpression(expr)
    assert parse_expression.list_result == expected_result


def test_failed_parse_expression():
    """ Тестирует разбор строки с ошибкой на лексемы """
    expr = "12+(23+5*(12-6)+37)+45d-(43-56*1274-(72+9))"
    with pytest.raises(ValueError):
        ParserExpression(expr)


@pytest.fixture(params=[
    ("12+23*8/4*3+4-6*4", [('NUMBER', 12), ('SIGN', '+'), ('NUMBER', 138.0), ('SIGN', '+'), ('NUMBER', 4), ('SIGN', '-'), ('NUMBER', 24)]),
    ("2*8/4", [('NUMBER', 4)]),
    ("3+4-8", [('NUMBER', 3), ('SIGN', '+'), ('NUMBER', 4), ('SIGN', '-'), ('NUMBER', 8)]),
    ("5*2 - 10/5", [('NUMBER', 10), ('SIGN', '-'), ('NUMBER', 2)])
],
ids=["12+23*8/4*3+4-6*4", "2*8/4", "3+4-8", "5*2 - 10/5"])
def process_multiplication_params(request):
    return request.param


def test_processing_multiplication(process_multiplication_params):
    """ Тестирует обработку умножений и деления """
    expr, expected_token_list = process_multiplication_params
    token_list = ParserExpression(expr).list_result
    calculator = Calculator()
    parsed_token_list = calculator._processing_multiplication_signs(token_list)
    assert parsed_token_list == expected_token_list


@pytest.fixture(params=[
    ("3+4-8", [('NUMBER', -1)]),
    ("2", [('NUMBER', 2)]),
    ("1+1+1", [('NUMBER', 3)]),
    ("2+2 - 4", [('NUMBER', 0)])
],
ids=["3+4-8", "2", "1+1+1", "2+2 - 4"])
def process_addition_params(request):
    return request.param


def test_processing_addition(process_addition_params):
    """ Тестирует обработку сложения и вычитания """
    expr, expected_token_list = process_addition_params
    token_list = ParserExpression(expr).list_result
    calculator = Calculator()
    parsed_token_list = calculator._processing_addition_signs(token_list)
    assert parsed_token_list == expected_token_list


@pytest.fixture(params=[
    ("(23+5*6/(12-9)+2)", ('NUMBER', 35)),
    ("324-2*112-(22+28)", ('NUMBER', 50)),
    ("12+35+45-50", ('NUMBER', 42)),
    ("12 + (23+5*6/(12-9)+2) + 45 - (324-2*112-(22+28))", ('NUMBER', 42))
],
ids=["(23+5*6/(12-9)+2)", "324-2*112-(22+28)", "12+35+45-50", "12 + (23+5*6/(12-9)+2) + 45 - (324-2*112-(22+28))"])
def process_parenthesis_params(request):
    return request.param


def test_processing_parenthesis(process_parenthesis_params):
    expr, expected_token_result = process_parenthesis_params
    parse_expression = ParserExpression(expr).list_result
    calculator = Calculator()
    token_result = calculator._processing_parenthesis(parse_expression)
    assert token_result == expected_token_result


@pytest.fixture(params=[
    ("(23+5*6/(12-9)+2)", 35),
    ("324-2*112-(22+28)", 50),
    ("12+35+45-50", 42),
    ("12 + (23+5*6/(12-9)+2) + 45 - (324-2*112-(22+28))", 42)
],
ids=["(23+5*6/(12-9)+2)", "324-2*112-(22+28)", "12+35+45-50", "12 + (23+5*6/(12-9)+2) + 45 - (324-2*112-(22+28))"])
def process_parsing_all_params(request):
    return request.param


def test_parsing_all(process_parsing_all_params):
    expr, expected_token_result = process_parsing_all_params
    calculator = Calculator()
    token_result = calculator._processing_all(expr)
    assert token_result == expected_token_result
