import unittest

def add(x, y):
    return x + y

class TestAdd(unittest.TestCase):
    def help_func(self):
        return "HELP"

    def test_add_positive(self):
        self.assertEqual(add(1, 2), 3)

    def test_add_negative(self):
        self.assertEqual(add(-1, -2), -3)

class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, x):
        self.value += x
        return self.value

    def sub(self, x):
        self.value -= x
        return self.value

class CalcTest(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def tearDown(self):
        del self.calc

    def test_add(self):
        self.assertEqual(self.calc.add(5), 5)
        self.assertEqual(self.calc.add(3), 8)
        self.assertEqual(self.calc.add(-2), 6)

    def test_sub(self):
        self.assertEqual(self.calc.sub(5), -5)