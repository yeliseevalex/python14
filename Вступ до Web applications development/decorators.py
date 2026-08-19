#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
ДЕКОРАТОРИ В PYTHON
===============================================================================

Що таке декоратор?

    Декоратор — це функція, яка отримує іншу функцію та змінює або розширює
    її поведінку, не змінюючи код самої функції.

    Простий приклад:

        def decorator(func):
            def wrapper():
                print("До виконання")
                func()
                print("Після виконання")

            return wrapper


        @decorator
        def hello():
            print("Hello")


    Запис:

        @decorator
        def hello():

    фактично означає:

        hello = decorator(hello)


Основна схема декоратора:

        def decorator(func):

            def wrapper(*args, **kwargs):

                # код ДО функції

                result = func(*args, **kwargs)

                # код ПІСЛЯ функції

                return result

            return wrapper


Навіщо потрібні декоратори?

    — логування;
    — перевірка прав доступу;
    — вимірювання часу виконання;
    — кешування;
    — перевірка типів;
    — валідація даних;
    — обробка помилок;
    — повторний запуск функції;
    — обмеження кількості викликів;
    — робота з API;
    — авторизація;
    — контроль параметрів.


Важливі поняття:

    @decorator
        Синтаксичний цукор для заміни функції декорованою версією.

    wrapper
        Внутрішня функція, яка обгортає оригінальну функцію.

    *args
        Дозволяє передати позиційні аргументи.

    **kwargs
        Дозволяє передати іменовані аргументи.

    functools.wraps
        Зберігає __name__, __doc__ та іншу інформацію оригінальної функції.

    nonlocal
        Дозволяє змінювати змінну із зовнішньої функції.

    @decorator(...)
        Декоратор, який сам приймає параметри.


===============================================================================
ШПАРГАЛКА
===============================================================================

    Простий декоратор:

        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper


    Декоратор з functools.wraps:

        from functools import wraps

        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper


    Декоратор з параметрами:

        def repeat(times):

            def decorator(func):

                @wraps(func)
                def wrapper(*args, **kwargs):
                    for _ in range(times):
                        func(*args, **kwargs)

                return wrapper

            return decorator


    Використання:

        @repeat(3)
        def hello():
            print("Hello")


    Фабрика декораторів:

        def decorator_factory(logger):

            def decorator(func):

                @wraps(func)
                def wrapper(*args, **kwargs):
                    logger(...)
                    return func(*args, **kwargs)

                return wrapper

            return decorator


===============================================================================
"""

import functools
import inspect
import re
import time


# =============================================================================
# 1. НАЙПРОСТІШИЙ ДЕКОРАТОР
# =============================================================================

def example_simple_decorator():
    """
    Найпростіший приклад декоратора.

    Декоратор додає код ДО та ПІСЛЯ виконання функції.
    """

    print("\n--- 1. Простий декоратор ---")

    def decorator(func):

        def wrapper():
            print("До виконання функції")

            func()

            print("Після виконання функції")

        return wrapper

    @decorator
    def hello():
        print("Hello World")

    hello()


# =============================================================================
# 2. ЩО НАСПРАВДІ РОБИТЬ @decorator
# =============================================================================

def example_decorator_syntax():
    """
    Показує, що:

        @decorator
        def hello():

    еквівалентно:

        hello = decorator(hello)
    """

    print("\n--- 2. Що відбувається з @decorator ---")

    def decorator(func):

        def wrapper():
            print("Wrapper працює")
            func()

        return wrapper

    def hello():
        print("Hello")

    # Замість @decorator пишемо вручну.
    hello = decorator(hello)

    hello()


# =============================================================================
# 3. ДЕКОРАТОР З *args І **kwargs
# =============================================================================

def example_args_kwargs():
    """
    *args та **kwargs дозволяють декоратору працювати
    з функціями з різною кількістю аргументів.
    """

    print("\n--- 3. *args та **kwargs ---")

    def decorator(func):

        def wrapper(*args, **kwargs):

            print("ARGS:", args)
            print("KWARGS:", kwargs)

            return func(*args, **kwargs)

        return wrapper

    @decorator
    def add(a, b):
        return a + b

    @decorator
    def greet(name, message="Hello"):
        return f"{message}, {name}"

    print("Результат:", add(5, 10))

    print(
        "Результат:",
        greet(
            name="Bob",
            message="Welcome"
        )
    )


# =============================================================================
# 4. ЧОМУ ПОТРІБЕН functools.wraps
# =============================================================================

def example_wraps():
    """
    Без functools.wraps декоратор замінює метадані оригінальної функції.

    Наприклад:

        function.__name__

    може стати:

        wrapper

    functools.wraps(func) виправляє це.
    """

    print("\n--- 4. functools.wraps ---")

    def decorator_without_wraps(func):

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @decorator_without_wraps
    def hello():
        """Документація функції hello."""

        print("Hello")

    print("Без wraps:")
    print("name:", hello.__name__)
    print("doc:", hello.__doc__)

    def decorator_with_wraps(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @decorator_with_wraps
    def hello_2():
        """Документація функції hello_2."""

        print("Hello 2")

    print("\nЗ wraps:")
    print("name:", hello_2.__name__)
    print("doc:", hello_2.__doc__)


# =============================================================================
# 5. ДЕКОРАТОР ДЛЯ ВИМІРЮВАННЯ ЧАСУ
# =============================================================================

def example_timer():
    """
    Практичний декоратор.

    Він вимірює, скільки часу займає виконання функції.
    """

    print("\n--- 5. Декоратор timer ---")

    def timer(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            print(
                f"\nSTART {func.__name__}".upper().center(
                    80,
                    "="
                )
            )

            start = time.time()

            result = func(*args, **kwargs)

            end = time.time()

            print(f"Result: {result}")
            print(
                f"Processing time: {end - start:.4f} seconds"
            )

            print("=" * 80)

            return result

        return wrapper

    @timer
    def add(a, b):
        return a + b

    @timer
    def multiply(a, b):
        return a * b

    @timer
    def power(x):
        time.sleep(1)
        return x ** 10

    add(5, 5)
    multiply(5, 5)
    power(5)


# =============================================================================
# 6. ДЕКОРАТОР З ЛІЧИЛЬНИКОМ ВИКЛИКІВ
# =============================================================================

def example_count_calls():
    """
    nonlocal дозволяє змінювати змінну count,
    яка знаходиться у зовнішній функції.

    Це приклад closure + decorator.
    """

    print("\n--- 6. Лічильник викликів ---")

    def count_calls(func):

        count = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            nonlocal count

            count += 1

            print(
                f"Функція {func.__name__} "
                f"викликана {count} разів"
            )

            return func(*args, **kwargs)

        return wrapper

    @count_calls
    def hello():
        print("Hello")

    hello()
    hello()
    hello()
    hello()


# =============================================================================
# 7. ДЕКОРАТОР З ПАРАМЕТРОМ
# =============================================================================

def example_repeat():
    """
    Декоратор repeat приймає параметр times.

    Тут вже три рівні:

        repeat()
            ↓
        decorator()
            ↓
        wrapper()
    """

    print("\n--- 7. Декоратор з параметром ---")

    def repeat(times):

        def decorator(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                for _ in range(times):
                    func(*args, **kwargs)

            return wrapper

        return decorator

    @repeat(3)
    def hello():
        print("Hello World")

    hello()


# =============================================================================
# 8. ФАБРИКА ДЕКОРАТОРІВ
# =============================================================================

def example_decorator_factory():
    """
    Функція може створювати декоратори.

    Це називається decorator factory.
    """

    print("\n--- 8. Фабрика декораторів ---")

    def error(message):
        print(f"[ERROR] {message}")

    def info(message):
        print(f"[INFO] {message}")

    def log_handler_factory(log_function):

        def decorator(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                try:
                    return func(*args, **kwargs)

                except Exception as error_object:

                    log_function(
                        f"Error in {func.__name__}: "
                        f"{error_object}"
                    )

                    return None

            return wrapper

        return decorator

    error_handler = log_handler_factory(error)
    info_handler = log_handler_factory(info)

    @error_handler
    def process_order(order):

        if order.get("amount", 0) <= 0:
            raise ValueError("Amount must be greater than 0")

        return "Order processed"

    @info_handler
    def process_payment(payment):

        if payment.get("amount", 0) <= 0:
            raise ValueError("Invalid payment")

        return "Payment processed"

    print(
        process_order(
            {"amount": 0}
        )
    )

    print(
        process_payment(
            {"amount": 100}
        )
    )


# =============================================================================
# 9. ДЕКОРАТОР ДЛЯ ОБРОБКИ ПОМИЛОК
# =============================================================================

def example_error_handler():
    """
    Декоратор перехоплює Exception.

    Тут добре видно взаємодію:

        try
        except
        else
        finally
        raise
    """

    print("\n--- 9. Обробка помилок через декоратор ---")

    def handle_errors(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:

                result = func(*args, **kwargs)

            except ValueError as error:

                print(
                    f"[VALUE ERROR] {error}"
                )

                return None

            except ZeroDivisionError:

                print(
                    "[ZERO DIVISION] "
                    "Не можна ділити на нуль"
                )

                return None

            except Exception as error:

                print(
                    f"[UNKNOWN ERROR] {error}"
                )

                return None

            else:
                print(
                    "Функція виконалась без помилки"
                )

                return result

            finally:
                print(
                    "finally: цей блок виконується "
                    "завжди"
                )

        return wrapper

    @handle_errors
    def divide(a, b):

        if a < 0:
            raise ValueError(
                "a не може бути від'ємним"
            )

        return a / b

    print("Результат:", divide(10, 2))

    print("Результат:", divide(10, 0))

    print("Результат:", divide(-5, 2))


# =============================================================================
# 10. ДЕКОРАТОР ДЛЯ ПЕРЕВІРКИ ПРАВ
# =============================================================================

def example_admin_only():
    """
    Декоратор може перевіряти права користувача
    перед виконанням функції.

    Це типовий приклад для веброзробки.
    """

    print("\n--- 10. Перевірка прав доступу ---")

    def admin_only(func):

        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):

            if user != "admin":

                print(
                    "403 Forbidden: "
                    "недостатньо прав"
                )

                return None

            return func(
                user,
                *args,
                **kwargs
            )

        return wrapper

    @admin_only
    def delete_user(user, username):

        print(
            f"{user} deleted {username}"
        )

    delete_user(
        "user",
        "bob"
    )

    delete_user(
        "admin",
        "bob"
    )

    print("\nМетадані функції:")
    print("name:", delete_user.__name__)
    print("doc:", delete_user.__doc__)


# =============================================================================
# 11. КЕШУВАННЯ РЕЗУЛЬТАТІВ
# =============================================================================

def example_cache():
    """
    Кеш дозволяє не виконувати повторно
    дорогу операцію для однакових аргументів.

    Приклад:

        calculate(5)

    виконується один раз.

    Наступний:

        calculate(5)

    бере результат із cache.
    """

    print("\n--- 11. Кешування ---")

    def cache(func):

        storage = {}

        @functools.wraps(func)
        def wrapper(*args):

            if args in storage:

                print(
                    f"Cache hit: {args}"
                )

                return storage[args]

            print(
                f"Calculate: {args}"
            )

            result = func(*args)

            storage[args] = result

            return result

        return wrapper

    @cache
    def calculate(number):

        time.sleep(1)

        return number * 10

    start = time.time()

    print(calculate(5))
    print(calculate(5))
    print(calculate(5))

    print(calculate(2))
    print(calculate(2))

    end = time.time()

    print(
        f"\nTotal time: "
        f"{end - start:.4f} seconds"
    )


# =============================================================================
# 12. ДЕКОРАТОР З REGEX — EMAIL
# =============================================================================

def example_validate_email():
    """
    Декоратор перевіряє email перед викликом функції.

    Тут поєднуються:

        decorator
        functools.wraps
        regex
        raise
    """

    print("\n--- 12. Regex + decorator: Email ---")

    def validate_email(func):

        @functools.wraps(func)
        def wrapper(email, *args, **kwargs):

            pattern = (
                r"^[\w.-]+@[\w.-]+\.\w+$"
            )

            if not re.fullmatch(
                pattern,
                email
            ):

                raise ValueError(
                    f"Invalid email: {email}"
                )

            return func(
                email,
                *args,
                **kwargs
            )

        return wrapper

    @validate_email
    def register(email):

        print(
            f"User {email} registered"
        )

    try:
        register(
            "user@gmail.com"
        )

        register(
            "wrong-email"
        )

    except ValueError as error:

        print(
            f"Помилка: {error}"
        )


# =============================================================================
# 13. УНІВЕРСАЛЬНИЙ REGEX-ДЕКОРАТОР
# =============================================================================

def example_regex_validate():
    """
    regex_validate(pattern)

    дозволяє передавати regex безпосередньо
    в декоратор.

    Наприклад:

        @regex_validate(r"\d{4}")

    означає:

        значення повинно складатися
        рівно з 4 цифр.
    """

    print("\n--- 13. Універсальний regex-декоратор ---")

    def regex_validate(pattern):

        def decorator(func):

            @functools.wraps(func)
            def wrapper(
                value,
                *args,
                **kwargs
            ):

                if not re.fullmatch(
                    pattern,
                    value
                ):

                    raise ValueError(
                        f"Value '{value}' "
                        f"doesn't match "
                        f"'{pattern}'"
                    )

                return func(
                    value,
                    *args,
                    **kwargs
                )

            return wrapper

        return decorator

    @regex_validate(
        r"\+380\d{9}"
    )
    def save_phone(value):

        print(
            f"Phone {value} saved"
        )

    @regex_validate(
        r"\d{4}"
    )
    def enter_pin(value):

        print(
            "Correct PIN"
        )

    save_phone(
        "+380991234567"
    )

    enter_pin(
        "1234"
    )


# =============================================================================
# 14. REGEX + ДЕКОРАТОР + ІМЕНОВАНІ ГРУПИ
# =============================================================================

def example_parse_user():
    """
    Декоратор може не тільки перевіряти дані,
    а й перетворювати їх перед передачею функції.

    Наприклад:

        User: Bob, Age: 30

    перетворюється на:

        name="Bob"
        age="30"
    """

    print("\n--- 14. Regex parsing + decorator ---")

    def parse_user(func):

        @functools.wraps(func)
        def wrapper(text):

            pattern = (
                r"User:\s*"
                r"(?P<name>\w+)"
                r",\s*Age:\s*"
                r"(?P<age>\d+)"
            )

            match = re.fullmatch(
                pattern,
                text
            )

            if not match:

                raise ValueError(
                    "Invalid user format"
                )

            data = match.groupdict()

            return func(
                **data
            )

        return wrapper

    @parse_user
    def create_user(name, age):

        print("Name:", name)
        print("Age:", age)

    create_user(
        "User: Bob, Age: 30"
    )


# =============================================================================
# 15. МАСКУВАННЯ НОМЕРА КАРТКИ
# =============================================================================

def example_mask_card():
    """
    Декоратор змінює значення аргументу
    перед передачею його функції.

    Було:

        1234 5678 9012 3456

    Стало:

        **** **** **** 3456
    """

    print("\n--- 15. Маскування банківської картки ---")

    def mask_card(func):

        @functools.wraps(func)
        def wrapper(
            card,
            *args,
            **kwargs
        ):

            masked = re.sub(
                r"\d{4}\s*\d{4}\s*\d{4}\s*(\d{4})",
                r"**** **** **** \1",
                card
            )

            return func(
                masked,
                *args,
                **kwargs
            )

        return wrapper

    @mask_card
    def enter_card(card):

        print(
            f"Card: {card}"
        )

    enter_card(
        "1234 5678 9012 3456"
    )


# =============================================================================
# 16. ОЧИЩЕННЯ ТЕКСТУ ЧЕРЕЗ REGEX
# =============================================================================

def example_clean_text():
    """
    Декоратор очищає HTML та зайві пробіли
    перед передачею тексту функції.
    """

    print("\n--- 16. Очищення тексту ---")

    def clean_text(func):

        @functools.wraps(func)
        def wrapper(
            text,
            *args,
            **kwargs
        ):

            # Видаляємо HTML-теги.
            text = re.sub(
                r"<[^>]+>",
                "",
                text
            )

            # Замінюємо декілька пробілів,
            # табуляції та перенесення рядка
            # одним пробілом.
            text = re.sub(
                r"\s+",
                " ",
                text
            )

            # Прибираємо пробіли на початку
            # та в кінці.
            text = text.strip()

            return func(
                text,
                *args,
                **kwargs
            )

        return wrapper

    @clean_text
    def save_description(text):

        print(
            repr(text)
        )

    save_description(
        """
        <p>Hello</p>
        <b>world</b>

        Python
        """
    )


# =============================================================================
# 17. ДЕКОРАТОР ДЛЯ ПЕРЕВІРКИ КІЛЬКОХ REGEX
# =============================================================================

def example_validate_multiple_fields():
    """
    Один декоратор може перевіряти
    одразу декілька параметрів функції.

    Наприклад:

        username
        email
        phone
    """

    print("\n--- 17. Валідація декількох параметрів ---")

    def validate(**patterns):

        def decorator(func):

            @functools.wraps(func)
            def wrapper(**kwargs):

                for name, pattern in patterns.items():

                    value = kwargs.get(name)

                    if value is None:
                        continue

                    if not isinstance(
                        value,
                        str
                    ):

                        raise TypeError(
                            f"{name} must be str"
                        )

                    if not re.fullmatch(
                        pattern,
                        value
                    ):

                        raise ValueError(
                            f"{name}={value} "
                            f"doesn't match "
                            f"{pattern}"
                        )

                return func(
                    **kwargs
                )

            return wrapper

        return decorator

    @validate(
        username=r"[a-zA-Z0-9_-]{3,20}",

        email=r"^[\w.-]+@[\w.-]+\.\w+$",

        phone=r"\+380\d{9}"
    )
    def register(
        username,
        email,
        phone
    ):

        print(
            f"Registered: {username}"
        )

    register(
        username="bob_user",
        email="bob@gmail.com",
        phone="+380123456789"
    )


# =============================================================================
# 18. ПЕРЕВІРКА ТИПІВ
# =============================================================================

def example_type_check():
    """
    Декоратор перевіряє типи аргументів
    перед виконанням функції.

    Для цього використовуємо inspect.signature().

    Це дозволяє правильно працювати
    як з позиційними, так і з іменованими аргументами.
    """

    print("\n--- 18. Перевірка типів ---")

    def type_check(**types):

        def decorator(func):

            @functools.wraps(func)
            def wrapper(
                *args,
                **kwargs
            ):

                # Отримуємо сигнатуру функції.
                signature = inspect.signature(
                    func
                )

                # Поєднуємо args та kwargs
                # з іменами параметрів.
                bound = signature.bind(
                    *args,
                    **kwargs
                )

                for name, value in (
                    bound.arguments.items()
                ):

                    # Якщо для цього параметра
                    # не вказаний тип — пропускаємо.
                    if name not in types:
                        continue

                    expected_type = types[name]

                    # Перевіряємо тип.
                    if not isinstance(
                        value,
                        expected_type
                    ):

                        raise TypeError(
                            f"{name} must be "
                            f"{expected_type.__name__}, "
                            f"but got "
                            f"{type(value).__name__}"
                        )

                return func(
                    *args,
                    **kwargs
                )

            return wrapper

        return decorator

    @type_check(
        name=str,
        age=int,
        price=float
    )
    def create_product(
        name,
        age,
        price
    ):

        print(
            "Product:",
            name
        )

        print(
            "Age:",
            age
        )

        print(
            "Price:",
            price
        )

    create_product(
        "iPhone",
        10,
        999.99
    )

    try:

        create_product(
            "iPhone",
            "10",
            999.99
        )

    except TypeError as error:

        print(
            "TypeError:",
            error
        )


# =============================================================================
# 19. ДЕКОРАТОР ПЕРЕВІРКИ ТИПІВ + REGEX
# =============================================================================

def example_type_and_regex():
    """
    Тут комбінуємо два підходи:

        1. Перевірка типу.
        2. Перевірка формату через regex.

    Це вже дуже близько до реального backend-коду.
    """

    print("\n--- 19. Type check + Regex ---")

    def validate_user(func):

        @functools.wraps(func)
        def wrapper(
            username,
            email
        ):

            # ---------------------------------------------------------
            # Перевірка типів
            # ---------------------------------------------------------

            if not isinstance(
                username,
                str
            ):

                raise TypeError(
                    "username must be str"
                )

            if not isinstance(
                email,
                str
            ):

                raise TypeError(
                    "email must be str"
                )

            # ---------------------------------------------------------
            # Перевірка username
            # ---------------------------------------------------------

            username_pattern = (
                r"[a-zA-Z0-9_-]{3,20}"
            )

            if not re.fullmatch(
                username_pattern,
                username
            ):

                raise ValueError(
                    "Invalid username"
                )

            # ---------------------------------------------------------
            # Перевірка email
            # ---------------------------------------------------------

            email_pattern = (
                r"^[\w.-]+@[\w.-]+\.\w+$"
            )

            if not re.fullmatch(
                email_pattern,
                email
            ):

                raise ValueError(
                    "Invalid email"
                )

            return func(
                username,
                email
            )

        return wrapper

    @validate_user
    def register_user(
        username,
        email
    ):

        print(
            f"User {username} "
            f"with {email} registered"
        )

    register_user(
        "bob_user",
        "bob@gmail.com"
    )


# =============================================================================
# 20. ДЕКОРАТОР З try / except / else / finally
# =============================================================================

def example_full_error_flow():
    """
    Повний приклад життєвого циклу виконання функції.

    try:
        Намагаємося виконати код.

    except:
        Обробляємо помилку.

    else:
        Виконується, якщо помилки не було.

    finally:
        Виконується завжди.
    """

    print(
        "\n--- 20. try / except / else / finally ---"
    )

    def safe_execution(func):

        @functools.wraps(func)
        def wrapper(
            *args,
            **kwargs
        ):

            print(
                f"\nЗапуск: {func.__name__}"
            )

            try:

                result = func(
                    *args,
                    **kwargs
                )

            except ValueError as error:

                print(
                    "ValueError:",
                    error
                )

                return None

            except ZeroDivisionError:

                print(
                    "ZeroDivisionError: "
                    "ділення на нуль"
                )

                return None

            else:

                print(
                    "Функція виконалась успішно"
                )

                return result

            finally:

                print(
                    "Ресурси можна звільнити "
                    "у finally"
                )

        return wrapper

    @safe_execution
    def calculate(a, b):

        if a < 0:

            raise ValueError(
                "a cannot be negative"
            )

        return a / b

    print(
        "Result:",
        calculate(10, 2)
    )

    print(
        "Result:",
        calculate(10, 0)
    )

    print(
        "Result:",
        calculate(-10, 2)
    )


# =============================================================================
# 21. ДЕКОРАТОР ДЛЯ ПОВТОРНОГО ВИКОНАННЯ ПРИ ПОМИЛЦІ
# =============================================================================

def example_retry():
    """
    Дуже практичний декоратор для API,
    HTTP-запитів, парсерів тощо.

    Якщо функція впала — повторюємо її
    декілька разів.
    """

    print(
        "\n--- 21. Retry decorator ---"
    )

    def retry(attempts):

        def decorator(func):

            @functools.wraps(func)
            def wrapper(
                *args,
                **kwargs
            ):

                last_error = None

                for attempt in range(
                    1,
                    attempts + 1
                ):

                    try:

                        print(
                            f"Attempt "
                            f"{attempt}/{attempts}"
                        )

                        return func(
                            *args,
                            **kwargs
                        )

                    except Exception as error:

                        last_error = error

                        print(
                            f"Error: {error}"
                        )

                # Якщо всі спроби завершилися
                # помилкою — передаємо останню.
                raise last_error

            return wrapper

        return decorator

    counter = 0

    @retry(3)
    def unstable_function():

        nonlocal_counter = None

        # Використовуємо зовнішню змінну
        # через список, щоб зберігати стан.
        return nonlocal_counter

    # Для демонстрації retry створимо
    # окрему функцію зі state.
    state = {
        "attempt": 0
    }

    @retry(3)
    def request_api():

        state["attempt"] += 1

        if state["attempt"] < 3:

            raise ConnectionError(
                "API unavailable"
            )

        return "API response"

    print(
        request_api()
    )


# =============================================================================
# 22. ОБМЕЖЕННЯ КІЛЬКОСТІ ВИКЛИКІВ
# =============================================================================

def example_rate_limit():
    """
    Простий rate limiter.

    Наприклад, після кожних 3 викликів
    робимо паузу.

    Такий підхід можна розширювати
    для API scraper'ів.
    """

    print(
        "\n--- 22. Rate limit ---"
    )

    def rate_limit(
        calls,
        delay
    ):

        def decorator(func):

            counter = 0

            @functools.wraps(func)
            def wrapper(
                *args,
                **kwargs
            ):

                nonlocal counter

                counter += 1

                if counter % calls == 0:

                    print(
                        f"Rate limit: "
                        f"sleep {delay}s"
                    )

                    time.sleep(delay)

                return func(
                    *args,
                    **kwargs
                )

            return wrapper

        return decorator

    @rate_limit(
        calls=3,
        delay=1
    )
    def request(number):

        print(
            f"Request {number}"
        )

    for i in range(1, 7):

        request(i)


# =============================================================================
# 23. ДЕКОРАТОРИ СТЕКАЮТЬСЯ
# =============================================================================

def example_multiple_decorators():
    """
    На одну функцію можна поставити
    декілька декораторів.

    Наприклад:

        @decorator_a
        @decorator_b
        def hello():

    Python читає це приблизно як:

        hello = decorator_a(
            decorator_b(
                hello
            )
        )
    """

    print(
        "\n--- 23. Кілька декораторів ---"
    )

    def first(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            print("FIRST: before")

            result = func(
                *args,
                **kwargs
            )

            print("FIRST: after")

            return result

        return wrapper

    def second(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            print("SECOND: before")

            result = func(
                *args,
                **kwargs
            )

            print("SECOND: after")

            return result

        return wrapper

    @first
    @second
    def hello():

        print("HELLO")

    hello()


# =============================================================================
# 24. ДЕКОРАТОР ДЛЯ РОУТИНГУ
# =============================================================================

def example_router():
    """
    Декоратори можна використовувати
    для створення простого router.

    Це нагадує те, як працюють
    Flask / FastAPI / Django-підходи.
    """

    print(
        "\n--- 24. Простий router ---"
    )

    routes = {}

    def route(
        method,
        path
    ):

        def decorator(func):

            routes[
                (method, path)
            ] = func

            return func

        return decorator

    @route(
        "GET",
        "/users"
    )
    def get_users():

        return "GET users"

    @route(
        "POST",
        "/users"
    )
    def create_user():

        return "POST user"

    print(
        routes[
            ("GET", "/users")
        ]()
    )

    print(
        routes[
            ("POST", "/users")
        ]()
    )


# =============================================================================
# 25. КОМБІНАЦІЯ: API + REGEX + TYPE CHECK + ERROR HANDLING
# =============================================================================

def example_real_project():
    """
    Фінальний приклад.

    Тут поєднуємо все, що вивчили:

        decorator
        wraps
        regex
        type checking
        raise
        try
        except
        else
        finally

    У реальному проєкті подібний підхід можна
    використовувати для API endpoint'ів,
    scraper'ів або сервісних функцій.
    """

    print(
        "\n--- 25. Комплексний приклад ---"
    )

    def validate_request(func):

        @functools.wraps(func)
        def wrapper(
            username,
            email
        ):

            try:

                # -----------------------------------------------------
                # 1. Перевірка типів
                # -----------------------------------------------------

                if not isinstance(
                    username,
                    str
                ):

                    raise TypeError(
                        "username must be str"
                    )

                if not isinstance(
                    email,
                    str
                ):

                    raise TypeError(
                        "email must be str"
                    )

                # -----------------------------------------------------
                # 2. Regex для username
                # -----------------------------------------------------

                username_pattern = (
                    r"[a-zA-Z0-9_-]{3,20}"
                )

                if not re.fullmatch(
                    username_pattern,
                    username
                ):

                    raise ValueError(
                        "Invalid username"
                    )

                # -----------------------------------------------------
                # 3. Regex для email
                # -----------------------------------------------------

                email_pattern = (
                    r"^[\w.-]+@[\w.-]+\.\w+$"
                )

                if not re.fullmatch(
                    email_pattern,
                    email
                ):

                    raise ValueError(
                        "Invalid email"
                    )

                # -----------------------------------------------------
                # 4. Виконання функції
                # -----------------------------------------------------

                result = func(
                    username,
                    email
                )

            except (
                TypeError,
                ValueError
            ) as error:

                print(
                    f"[ERROR] {error}"
                )

                return None

            else:

                print(
                    "[INFO] Request successful"
                )

                return result

            finally:

                print(
                    "[INFO] Request finished"
                )

        return wrapper

    @validate_request
    def register(
        username,
        email
    ):

        return {
            "status": "success",
            "username": username,
            "email": email
        }

    print(
        register(
            "alex",
            "alex@gmail.com"
        )
    )

    print(
        register(
            "a",
            "wrong-email"
        )
    )

    print(
        register(
            123,
            "alex@gmail.com"
        )
    )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    # Базові декоратори
    example_simple_decorator()
    example_decorator_syntax()
    example_args_kwargs()
    example_wraps()

    # Практичні декоратори
    example_timer()
    example_count_calls()
    example_repeat()
    example_decorator_factory()

    # Обробка помилок
    example_error_handler()
    example_admin_only()

    # Кешування
    example_cache()

    # Regex + decorators
    example_validate_email()
    example_regex_validate()
    example_parse_user()
    example_mask_card()
    example_clean_text()
    example_validate_multiple_fields()

    # Type checking
    example_type_check()
    example_type_and_regex()

    # try / except / else / finally / raise
    example_full_error_flow()

    # Більш практичні декоратори
    example_retry()
    example_rate_limit()

    # Складніші конструкції
    example_multiple_decorators()
    example_router()

    # Фінальний комплексний приклад
    example_real_project()