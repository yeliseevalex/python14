import pytest

from test_unittest_example import Calculator


def add(x :int, y:int) -> int:
    return x + y

def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0

def test_add_mixed():
    assert add(-1, 2) == 1

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, -2, -3),
    (0, 0, 0),
    (-1, 2, 1)
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

def test_sum(sample_list):
    assert sum(sample_list) == 15

def calc(operation, a, b):
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return a / b

@pytest.mark.parametrize("operation, a, b, expected", [
    ("+", 1, 2, 3),
    ("-", -1, -2, 1),
    ("*", 0, 0, 0),
    ("/", -1, 2, -0.5)
])
def test_add_param(operation, a, b, expected):
    assert calc(operation, a, b) == expected


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def test_divide_error():
    with pytest.raises(ZeroDivisionError):
        divide(1, "0")

def split_text(text, delimiter=" "):
    if not isinstance(delimiter, str):
        raise TypeError("delimiter is not a string")
    return text.split(delimiter)

def test_split_text():
    text = "this;is;a;test"
    with pytest.raises(TypeError):
        split_text(text, 1)
    assert split_text(text, ";") == ["this", "is", "a", "test"]
