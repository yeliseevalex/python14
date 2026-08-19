#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
ВИКЛЮЧЕННЯ, DECORATORS, REGEX ТА ВЛАСНІ КЛАСИ ПОМИЛОК
===============================================================================

У цьому файлі ми поступово розглянемо:

    1. Що таке exception.
    2. try / except.
    3. else.
    4. finally.
    5. raise.
    6. assert.
    7. Передачу виключень між функціями.
    8. Власні класи виключень.
    9. Декоратори для обробки помилок.
    10. Regex-валідацію.
    11. Валідацію даних перед створенням об'єкта.
    12. Роботу з класами.
    13. Практичний мініпроєкт.

-------------------------------------------------------------------------------
ЩО ТАКЕ EXCEPTION?
-------------------------------------------------------------------------------

Exception — це об'єкт, який повідомляє програмі, що під час виконання
виникла помилка або нестандартна ситуація.

Наприклад:

    10 / 0

викличе:

    ZeroDivisionError


Якщо помилку не обробити:

    def divide(a, b):
        return a / b

    divide(10, 0)

програма завершить роботу з помилкою.


-------------------------------------------------------------------------------
TRY / EXCEPT
-------------------------------------------------------------------------------

try:

    Код, у якому може виникнути помилка.

except:

    Код, який виконається, якщо помилка виникла.


Приклад:

    try:
        result = 10 / 0

    except ZeroDivisionError:
        print("Не можна ділити на нуль")


-------------------------------------------------------------------------------
ELSE
-------------------------------------------------------------------------------

else виконується тільки тоді, коли в try НЕ виникла помилка.

    try:
        result = 10 / 2

    except ZeroDivisionError:
        print("Помилка")

    else:
        print("Все добре")


-------------------------------------------------------------------------------
FINALLY
-------------------------------------------------------------------------------

finally виконується завжди:

    try:
        ...
    except:
        ...
    finally:
        ...


Його часто використовують для:

    — закриття файлів;
    — закриття з'єднання з БД;
    — звільнення ресурсів;
    — завершального логування.


-------------------------------------------------------------------------------
RAISE
-------------------------------------------------------------------------------

raise дозволяє самостійно створити виключення.

    if age < 18:
        raise ValueError("User must be 18+")


-------------------------------------------------------------------------------
ВЛАСНІ ВИКЛЮЧЕННЯ
-------------------------------------------------------------------------------

Можна створювати власні класи помилок:

    class UserError(Exception):
        pass


А потім:

    raise UserError("User not found")


Це дозволяє відрізняти різні типи помилок.

-------------------------------------------------------------------------------
У ФІНАЛЬНОМУ ПРИКЛАДІ
-------------------------------------------------------------------------------

Ми об'єднаємо все:

    User
        ↓
    UserService
        ↓
    Regex validation
        ↓
    Custom exceptions
        ↓
    try / except / else / finally
        ↓
    Decorator
        ↓
    Logging


===============================================================================
"""


import re
from functools import wraps
import time


# =============================================================================
# 1. ПРОСТЕ ВИКЛЮЧЕННЯ
# =============================================================================

def example_without_exception():
    """
    Якщо викликати функцію без обробки виключення,
    програма завершиться з помилкою.
    """

    print("\n--- 1. Функція без обробки exception ---")

    def divide(a, b):
        return a / b

    # Якщо розкоментувати:

    # print(divide(10, 0))

    # Отримаємо:
    #
    # ZeroDivisionError:
    # division by zero

    print(
        "Приклад із діленням:",
        divide(10, 2)
    )


# =============================================================================
# 2. TRY / EXCEPT
# =============================================================================

def example_try_except():
    """
    try дозволяє виконати потенційно небезпечний код.

    except перехоплює помилку.
    """

    print("\n--- 2. try / except ---")

    def divide(a, b):

        try:

            return a / b

        except ZeroDivisionError:

            print(
                "ERROR: division by zero"
            )

            return None

    print(
        divide(10, 2)
    )

    print(
        divide(10, 0)
    )


# =============================================================================
# 3. TRY / EXCEPT / ELSE / FINALLY
# =============================================================================

def example_try_except_else_finally():
    """
    Повна конструкція обробки виключення.

    try:
        основний код

    except:
        обробка помилки

    else:
        виконується, якщо помилки НЕ було

    finally:
        виконується ЗАВЖДИ
    """

    print(
        "\n--- 3. try / except / else / finally ---"
    )

    def divide(a, b):

        try:

            result = a / b

        except ZeroDivisionError:

            print(
                "ERROR: division by zero"
            )

            return None

        else:

            print(
                "Success"
            )

            return result

        finally:

            print(
                "Operation is finished"
            )

    print(
        "Result:",
        divide(10, 2)
    )

    print(
        "Result:",
        divide(10, 0)
    )


# =============================================================================
# 4. RAISE
# =============================================================================

def example_raise():
    """
    raise дозволяє програмісту самостійно
    викликати exception.

    Це корисно, коли Python сам не вважає
    ситуацію помилкою, але для нашої бізнес-логіки
    вона є помилкою.
    """

    print(
        "\n--- 4. raise ---"
    )

    def check_age(age):

        if age < 0:

            raise ValueError(
                "Age cannot be negative"
            )

        return age

    print(
        check_age(25)
    )

    try:

        print(
            check_age(-10)
        )

    except ValueError as error:

        print(
            "Помилка:",
            error
        )


# =============================================================================
# 5. ASSERT
# =============================================================================

def example_assert():
    """
    assert використовується для перевірки
    певного припущення.

    Якщо умова False — виникає AssertionError.
    """

    print(
        "\n--- 5. assert ---"
    )

    def calculate_average(numbers):

        assert (
            len(numbers) > 0
        ), "numbers must not be empty"

        return (
            sum(numbers)
            / len(numbers)
        )

    print(
        calculate_average(
            [10, 20, 30]
        )
    )

    try:

        calculate_average([])

    except AssertionError as error:

        print(
            "AssertionError:",
            error
        )


# =============================================================================
# 6. ПЕРЕДАЧА EXCEPTION МІЖ ФУНКЦІЯМИ
# =============================================================================

def example_exception_propagation():
    """
    Exception може виникнути глибоко
    всередині викликів функцій.

        function_a()
            ↓
        function_b()
            ↓
        function_c()
            ↓
        raise ValueError

    Якщо function_c не обробить помилку,
    вона піде вище до function_b,
    потім до function_a.
    """

    print(
        "\n--- 6. Передача exception між функціями ---"
    )

    def function_c():

        raise KeyError(
            "Missing key in JSON"
        )

    def function_b():

        function_c()

    def function_a():

        try:

            function_b()

        except KeyError as error:

            print(
                "Помилка перехоплена "
                f"у function_a: {error}"
            )

    function_a()


# =============================================================================
# 7. ВЛАСНИЙ КЛАС ВИКЛЮЧЕННЯ
# =============================================================================

def example_custom_exception():
    """
    Власні exception-класи дозволяють
    створювати зрозумілу структуру помилок.
    """

    print(
        "\n--- 7. Власний exception ---"
    )

    class AuthenticationError(Exception):
        """
        Помилка авторизації.
        """

        def __init__(
            self,
            message="Authentication Error"
        ):

            super().__init__(
                message
            )

    def authenticate_user(
        username,
        password
    ):

        if (
            username != "admin"
            or password != "12345"
        ):

            raise AuthenticationError(
                "Invalid username or password"
            )

        return True

    try:

        print(
            authenticate_user(
                "admin",
                "1234"
            )
        )

    except AuthenticationError as error:

        print(
            "AuthenticationError:",
            error
        )


# =============================================================================
# 8. ІЄРАРХІЯ ВЛАСНИХ EXCEPTION
# =============================================================================

def example_exception_hierarchy():
    """
    Власні помилки можна будувати
    у вигляді ієрархії.

        Exception
            ↓
        UserError
            ↓
        ValidationError
        UserAlreadyExists

    Це дозволяє перехоплювати як конкретну,
    так і загальну помилку.
    """

    print(
        "\n--- 8. Ієрархія exception ---"
    )

    class UserError(Exception):
        pass

    class ValidationError(UserError):
        pass

    class UserAlreadyExists(UserError):
        pass

    def register_user(
        username,
        exists=False
    ):

        if len(username) < 3:

            raise ValidationError(
                "Username too short"
            )

        if exists:

            raise UserAlreadyExists(
                "User already exists"
            )

        return "User registered"

    try:

        print(
            register_user(
                "Bob",
                exists=True
            )
        )

    except ValidationError as error:

        print(
            "ValidationError:",
            error
        )

    except UserAlreadyExists as error:

        print(
            "UserAlreadyExists:",
            error
        )

    except UserError as error:

        print(
            "UserError:",
            error
        )


# =============================================================================
# 9. DECORATOR ДЛЯ ЛОГУВАННЯ ПОМИЛОК
# =============================================================================

def example_log_errors():
    """
    Декоратор дозволяє централізовано
    логувати помилки функцій.
    """

    print(
        "\n--- 9. Decorator для логування ---"
    )

    def log_errors(func):

        @wraps(func)
        def wrapper(
            *args,
            **kwargs
        ):

            try:

                result = func(
                    *args,
                    **kwargs
                )

            except Exception as error:

                print(
                    f"[LOG] "
                    f"Помилка у "
                    f"{func.__name__}: "
                    f"{error}"
                )

                # raise повторно передає
                # те саме exception далі.
                raise

            finally:

                print(
                    f"[LOG] Функція "
                    f"{func.__name__} "
                    f"завершила роботу"
                )

            return result

        return wrapper

    @log_errors
    def divide(a, b):

        return a / b

    try:

        divide(10, 0)

    except ZeroDivisionError:

        print(
            "Помилка перехоплена "
            "зовні декоратора"
        )


# =============================================================================
# 10. REGEX — ВАЛІДАЦІЯ USERNAME
# =============================================================================

def example_regex_username():
    """
    Перевіряємо username через regex.

    Умова:

        3-20 символів

    Дозволені:

        a-z
        A-Z
        0-9
        _
    """

    print(
        "\n--- 10. Regex: username ---"
    )

    pattern = (
        r"^[a-zA-Z0-9_]{3,20}$"
    )

    usernames = [
        "bob_123",
        "john",
        "ab",
        "user@email",
        "very_long_username_123"
    ]

    for username in usernames:

        if re.fullmatch(
            pattern,
            username
        ):

            print(
                username,
                "— OK"
            )

        else:

            print(
                username,
                "— INVALID"
            )


# =============================================================================
# 11. REGEX — ВАЛІДАЦІЯ EMAIL
# =============================================================================

def example_regex_email():
    """
    Простий навчальний regex для email.
    """

    print(
        "\n--- 11. Regex: email ---"
    )

    pattern = (
        r"^[\w.-]+@[\w.-]+\.\w+$"
    )

    emails = [
        "bob@gmail.com",
        "john@example.org",
        "john@gmail",
        "wrong-email"
    ]

    for email in emails:

        if re.fullmatch(
            pattern,
            email
        ):

            print(
                email,
                "— OK"
            )

        else:

            print(
                email,
                "— INVALID"
            )


# =============================================================================
# 12. REGEX — ПАРОЛЬ
# =============================================================================

def example_regex_password():
    """
    Перевіряємо пароль.

    Умова:

        мінімум 8 символів
        хоча б одна велика літера
        хоча б одна маленька літера
        хоча б одна цифра
    """

    print(
        "\n--- 12. Regex: password ---"
    )

    def validate_password(password):

        if len(password) < 8:

            raise ValueError(
                "Password must contain "
                "at least 8 characters"
            )

        if not re.search(
            r"[A-Z]",
            password
        ):

            raise ValueError(
                "Password must contain "
                "an uppercase letter"
            )

        if not re.search(
            r"[a-z]",
            password
        ):

            raise ValueError(
                "Password must contain "
                "a lowercase letter"
            )

        if not re.search(
            r"\d",
            password
        ):

            raise ValueError(
                "Password must contain "
                "a number"
            )

        return True

    passwords = [
        "Python123",
        "python123",
        "PYTHON123",
        "Python",
        "12345678"
    ]

    for password in passwords:

        try:

            validate_password(
                password
            )

        except ValueError as error:

            print(
                password,
                "—",
                error
            )

        else:

            print(
                password,
                "— OK"
            )


# =============================================================================
# 13. КЛАС USER
# =============================================================================

def example_user_class():
    """
    Простий клас користувача.
    """

    print(
        "\n--- 13. Клас User ---"
    )

    class User:

        def __init__(
            self,
            username,
            email,
            age
        ):

            self.username = username
            self.email = email
            self.age = age

        def __str__(self):

            return (
                f"{self.username} "
                f"<{self.email}>"
            )

    user = User(
        "bob",
        "bob@gmail.com",
        25
    )

    print(user)


# =============================================================================
# 14. USER SERVICE
# =============================================================================

def example_user_service():
    """
    UserService відповідає за роботу
    зі списком користувачів.

    Це окремий клас, тому бізнес-логіка
    не знаходиться безпосередньо
    всередині User.
    """

    print(
        "\n--- 14. UserService ---"
    )

    class User:

        def __init__(
            self,
            username,
            email
        ):

            self.username = username
            self.email = email

        def __str__(self):

            return (
                f"{self.username} "
                f"<{self.email}>"
            )

    class UserService:

        def __init__(self):

            self.users = []

        def find_by_email(
            self,
            email
        ):

            for user in self.users:

                if user.email == email:

                    return user

            return None

        def add_user(
            self,
            user
        ):

            if self.find_by_email(
                user.email
            ):

                raise ValueError(
                    "User already exists"
                )

            self.users.append(
                user
            )

        def get_all_users(self):

            return self.users

    service = UserService()

    service.add_user(
        User(
            "bob",
            "bob@gmail.com"
        )
    )

    print(
        service.find_by_email(
            "bob@gmail.com"
        )
    )

    print(
        "\nAll users:"
    )

    for user in service.get_all_users():

        print(user)


# =============================================================================
# 15. ФІНАЛЬНА ПРАКТИЧНА ЗАДАЧА
# =============================================================================

"""
===============================================================================
ПРАКТИЧНА ЗАДАЧА
===============================================================================

                    USER REGISTRATION SERVICE
===============================================================================

Створіть систему реєстрації користувачів.

Вона повинна використовувати:

    класи;
    власні exception;
    try / except / else / finally;
    raise;
    regex;
    декоратор;
    functools.wraps.

-------------------------------------------------------------------------------
УМОВА
-------------------------------------------------------------------------------

Необхідно реалізувати клас User:

    User(
        username,
        email,
        age,
        password
    )


Користувач має містити:

    username
    email
    age
    password


-------------------------------------------------------------------------------
1. USERNAME
-------------------------------------------------------------------------------

Username повинен:

    — містити від 3 до 20 символів;
    — містити тільки:
        латинські літери
        цифри
        _


Приклади:

    bob_123       -> OK
    john          -> OK
    user_2026     -> OK

    bo            -> ERROR
    user@email    -> ERROR
    user-name     -> ERROR


Regex:

    r"^[a-zA-Z0-9_]{3,20}$"


-------------------------------------------------------------------------------
2. EMAIL
-------------------------------------------------------------------------------

Email повинен мати приблизно такий формат:

    username@domain.com


Приклади:

    bob@gmail.com       -> OK
    john@example.org    -> OK

    john@gmail          -> ERROR
    wrong-email         -> ERROR


Використати regex:

    r"^[\w.-]+@[\w.-]+\.\w+$"


-------------------------------------------------------------------------------
3. AGE
-------------------------------------------------------------------------------

Користувач повинен бути повнолітнім.

    age >= 18


Якщо:

    age < 18

необхідно:

    raise ValidationError(...)


-------------------------------------------------------------------------------
4. PASSWORD
-------------------------------------------------------------------------------

Пароль повинен:

    — містити мінімум 8 символів;
    — містити хоча б одну велику літеру;
    — містити хоча б одну маленьку літеру;
    — містити хоча б одну цифру.


Наприклад:

    Python123      -> OK
    Hello2026      -> OK

    python123      -> ERROR
    PYTHON123      -> ERROR
    Python         -> ERROR
    12345678       -> ERROR


-------------------------------------------------------------------------------
5. ВЛАСНІ EXCEPTION
-------------------------------------------------------------------------------

Створіть:

    class UserError(Exception):
        pass


Від нього успадкуйте:

    class ValidationError(UserError):
        ...


    class UserAlreadyExists(UserError):
        pass


ValidationError повинна мати:

    message
    field


Наприклад:

    raise ValidationError(
        "Некоректний email",
        field="email"
    )


При виведенні:

    [email] Некоректний email


-------------------------------------------------------------------------------
6. USER SERVICE
-------------------------------------------------------------------------------

Створіть:

    class UserService:


У ньому повинні бути методи:

    find_by_email(email)

    add_user(user)

    remove_user(email)

    get_all_users()


-------------------------------------------------------------------------------
7. ЗАБОРОНА ДУБЛІКАТІВ
-------------------------------------------------------------------------------

Якщо користувач із таким email вже існує:

    raise UserAlreadyExists(
        "Користувач з таким email вже існує"
    )


-------------------------------------------------------------------------------
8. DECORATOR
-------------------------------------------------------------------------------

Створіть декоратор:

    @log_errors


Він повинен:

    1. виконувати функцію;
    2. перехоплювати Exception;
    3. друкувати помилку;
    4. використовувати raise, щоб передати
       exception далі;
    5. у finally повідомляти,
       що функція завершила роботу.


Приклад:

    @log_errors
    def register_user(...):
        ...


-------------------------------------------------------------------------------
9. REGISTER_USER
-------------------------------------------------------------------------------

Створіть:

    register_user(
        service,
        username,
        email,
        age,
        password
    )


Усередині:

    try:

        validate_username(...)
        validate_email(...)
        validate_age(...)
        validate_password(...)

        user = User(...)

        service.add_user(user)


    except ValidationError:
        ...


    except UserAlreadyExists:
        ...


    except Exception:
        ...


    else:
        ...


    finally:
        ...


-------------------------------------------------------------------------------
10. SHOW_USER
-------------------------------------------------------------------------------

Створіть:

    show_user(
        service,
        email
    )


Якщо користувача немає:

    raise UserError(
        "Користувача не знайдено"
    )


Використати:

    try
    except
    else
    finally


-------------------------------------------------------------------------------
11. DELETE_USER
-------------------------------------------------------------------------------

Створіть:

    delete_user(
        service,
        email
    )


Якщо користувача немає:

    raise UserError(...)


Якщо існує:

    видалити його зі списку.


-------------------------------------------------------------------------------
12. ТЕСТОВІ ДАНІ
-------------------------------------------------------------------------------

Програма повинна перевірити щонайменше такі випадки:


1.

    register_user(
        service,
        "bob_123",
        "bob@gmail.com",
        25,
        "Python12345"
    )

    Очікується:
        успішна реєстрація


2.

    register_user(
        service,
        "bo",
        "bob2@gmail.com",
        25,
        "Python12345"
    )

    Очікується:
        помилка username


3.

    register_user(
        service,
        "john",
        "john@gmail",
        25,
        "Python12345"
    )

    Очікується:
        помилка email


4.

    register_user(
        service,
        "mike",
        "mike@gmail.com",
        15,
        "Python12345"
    )

    Очікується:
        помилка age


5.

    register_user(
        service,
        "mike",
        "mike@gmail.com",
        25,
        "123456789P"
    )

    Очікується:
        помилка password


6.

    register_user(
        service,
        "mike",
        "mike@gmail.com",
        25,
        "Python12345"
    )

    Очікується:
        успішна реєстрація


7.

    register_user(
        service,
        "second_bob",
        "bob@gmail.com",
        25,
        "Python12345"
    )

    Очікується:
        UserAlreadyExists


8.

    show_user(
        service,
        "bob@gmail.com"
    )

    Очікується:
        користувача знайдено


9.

    show_user(
        service,
        "unknown@gmail.com"
    )

    Очікується:
        UserError


10.

    delete_user(
        service,
        "mike@gmail.com"
    )

    Очікується:
        користувача видалено


11.

    delete_user(
        service,
        "mike@gmail.com"
    )

    Очікується:
        UserError


-------------------------------------------------------------------------------
ДОДАТКОВЕ ЗАВДАННЯ
-------------------------------------------------------------------------------

Після реалізації основної задачі додайте декоратор:

    @type_check


який перевірятиме типи аргументів.

Наприклад:

    @type_check(
        username=str,
        email=str,
        age=int,
        password=str
    )
    def register_user(...):
        ...


Якщо передали:

    age="25"


має виникнути:

    TypeError


-------------------------------------------------------------------------------
ЩЕ ОДНЕ ДОДАТКОВЕ ЗАВДАННЯ
-------------------------------------------------------------------------------

Додайте декоратор:

    @timer


який вимірює час виконання:

    register_user()
    show_user()
    delete_user()


У результаті повинно бути приблизно:

    [TIMER]
    register_user -> 0.00001 sec


Таким чином фінальна програма повинна поєднати:

    REGEX
       +
    DECORATORS
       +
    EXCEPTIONS
       +
    CLASSES
       +
    try / except / else / finally
       +
    raise
       +
    VALIDATION

===============================================================================
"""


# =============================================================================
# 16. РІШЕННЯ ФІНАЛЬНОЇ ЗАДАЧІ
# =============================================================================

def example_final_project():
    """
    Повна реалізація практичної задачі.

    Тут ми вже не просто демонструємо окремі конструкції,
    а використовуємо їх разом у невеликому проєкті.
    """

    print(
        "\n"
        + "=" * 70
    )

    print(
        "ФІНАЛЬНИЙ ПРОЄКТ: USER SERVICE"
    )

    print(
        "=" * 70
    )

    # =========================================================================
    # ВЛАСНІ ВИКЛЮЧЕННЯ
    # =========================================================================

    class UserError(Exception):
        """
        Базова помилка, пов'язана з користувачем.

        Від неї будуть успадковуватися
        інші типи помилок.
        """

        pass


    class ValidationError(UserError):
        """
        Помилка валідації.

        field дозволяє знати,
        яке саме поле неправильне.
        """

        def __init__(
            self,
            message,
            field=None
        ):

            super().__init__(
                message
            )

            self.message = message
            self.field = field

        def __str__(self):

            if self.field:

                return (
                    f"[{self.field}] "
                    f"{self.message}"
                )

            return self.message


    class UserAlreadyExists(UserError):
        """
        Помилка, якщо email вже існує.
        """

        pass


    # =========================================================================
    # КЛАС USER
    # =========================================================================

    class User:

        def __init__(
            self,
            username,
            email,
            age,
            password
        ):

            self.username = username
            self.email = email
            self.age = age

            # У реальному production-коді пароль
            # не можна зберігати у відкритому вигляді.
            #
            # Тут це зроблено тільки
            # для навчальної демонстрації.
            self.password = password

        def __str__(self):

            return (
                f"{self.username} "
                f"<{self.email}>"
            )


    # =========================================================================
    # USER SERVICE
    # =========================================================================

    class UserService:

        def __init__(self):

            # Тут зберігаємо користувачів.
            #
            # У реальному проєкті замість списку
            # зазвичай буде база даних.
            self.users = []


        def find_by_email(
            self,
            email
        ):

            for user in self.users:

                if user.email == email:

                    return user

            return None


        def add_user(
            self,
            user
        ):

            # Перевіряємо,
            # чи існує такий email.
            if self.find_by_email(
                user.email
            ):

                raise UserAlreadyExists(
                    "Користувач з таким "
                    "email вже існує"
                )

            self.users.append(
                user
            )


        def remove_user(
            self,
            email
        ):

            user = self.find_by_email(
                email
            )

            if not user:

                raise UserError(
                    "Користувача з таким "
                    "email не знайдено"
                )

            self.users.remove(
                user
            )

            return user


        def get_all_users(self):

            return self.users


    # =========================================================================
    # DECORATOR LOG_ERRORS
    # =========================================================================

    def log_errors(func):
        """
        Декоратор логування.

        Важливий момент:

            raise

        без аргументів повторно передає
        поточний exception.

        Тобто декоратор не "з'їдає"
        помилку.
        """

        @wraps(func)
        def wrapper(
            *args,
            **kwargs
        ):

            try:

                result = func(
                    *args,
                    **kwargs
                )

            except Exception as error:

                print(
                    f"[LOG] Помилка "
                    f"у {func.__name__}: "
                    f"{error}"
                )

                # Передаємо помилку далі.
                raise

            finally:

                print(
                    f"[LOG] Функція "
                    f"{func.__name__} "
                    f"завершила роботу"
                )

            return result

        return wrapper


    # =========================================================================
    # VALIDATE USERNAME
    # =========================================================================

    def validate_username(
        username
    ):
        """
        Username:

            3-20 символів

        Дозволені:

            a-z
            A-Z
            0-9
            _
        """

        pattern = (
            r"^[a-zA-Z0-9_]{3,20}$"
        )

        if not re.fullmatch(
            pattern,
            username
        ):

            raise ValidationError(
                (
                    "Username повинен "
                    "містити 3-20 символів "
                    "та складатися з букв, "
                    "цифр та _"
                ),
                field="username"
            )


    # =========================================================================
    # VALIDATE EMAIL
    # =========================================================================

    def validate_email(
        email
    ):
        """
        Перевірка email через regex.
        """

        pattern = (
            r"^[\w.-]+@[\w.-]+\.\w+$"
        )

        if not re.fullmatch(
            pattern,
            email
        ):

            raise ValidationError(
                "Некоректний email",
                field="email"
            )


    # =========================================================================
    # VALIDATE AGE
    # =========================================================================

    def validate_age(
        age
    ):
        """
        Користувач повинен бути
        не молодше 18 років.
        """

        if age < 18:

            raise ValidationError(
                (
                    "Користувач повинен "
                    "бути старше 18 років"
                ),
                field="age"
            )


    # =========================================================================
    # VALIDATE PASSWORD
    # =========================================================================

    def validate_password(
        password
    ):
        """
        Пароль повинен:

            1. Мати мінімум 8 символів.
            2. Мати велику літеру.
            3. Мати маленьку літеру.
            4. Мати цифру.
        """

        if len(password) < 8:

            raise ValidationError(
                (
                    "Пароль повинен містити "
                    "мінімум 8 символів"
                ),
                field="password"
            )


        if not re.search(
            r"[A-Z]",
            password
        ):

            raise ValidationError(
                (
                    "Пароль повинен містити "
                    "хоча б одну велику літеру"
                ),
                field="password"
            )


        if not re.search(
            r"[a-z]",
            password
        ):

            raise ValidationError(
                (
                    "Пароль повинен містити "
                    "хоча б одну маленьку літеру"
                ),
                field="password"
            )


        if not re.search(
            r"\d",
            password
        ):

            raise ValidationError(
                (
                    "Пароль повинен містити "
                    "хоча б одну цифру"
                ),
                field="password"
            )


    # =========================================================================
    # REGISTER USER
    # =========================================================================

    @log_errors
    def register_user(
        service,
        username,
        email,
        age,
        password
    ):

        print(
            "\n"
            + "=" * 50
        )

        print(
            "ПОЧАТОК РЕЄСТРАЦІЇ"
        )

        print(
            "=" * 50
        )


        try:

            # ---------------------------------------------------------------
            # КРОК 1
            # Перевіряємо username.
            # ---------------------------------------------------------------

            validate_username(
                username
            )


            # ---------------------------------------------------------------
            # КРОК 2
            # Перевіряємо email.
            # ---------------------------------------------------------------

            validate_email(
                email
            )


            # ---------------------------------------------------------------
            # КРОК 3
            # Перевіряємо age.
            # ---------------------------------------------------------------

            validate_age(
                age
            )


            # ---------------------------------------------------------------
            # КРОК 4
            # Перевіряємо password.
            # ---------------------------------------------------------------

            validate_password(
                password
            )


            # ---------------------------------------------------------------
            # КРОК 5
            # Якщо всі перевірки пройшли,
            # створюємо User.
            # ---------------------------------------------------------------

            user = User(
                username=username,
                email=email,
                age=age,
                password=password
            )


            # ---------------------------------------------------------------
            # КРОК 6
            # Додаємо користувача.
            #
            # Тут може виникнути:
            #
            # UserAlreadyExists
            # ---------------------------------------------------------------

            service.add_user(
                user
            )


        # =========================================================================
        # Якщо проблема з даними.
        # =========================================================================

        except ValidationError as error:

            print(
                f"Помилка валідації: "
                f"{error}"
            )


        # =========================================================================
        # Якщо email вже використовується.
        # =========================================================================

        except UserAlreadyExists as error:

            print(
                f"Помилка: {error}"
            )


        # =========================================================================
        # Будь-яка інша невідома помилка.
        # =========================================================================

        except Exception as error:

            print(
                f"Невідома помилка: "
                f"{error}"
            )


        # =========================================================================
        # Виконається тільки якщо НЕ було exception.
        # =========================================================================

        else:

            print(
                f"Користувача "
                f"{user.username} "
                f"успішно зареєстровано!"
            )


        # =========================================================================
        # Виконається завжди.
        # =========================================================================

        finally:

            print(
                "Операція реєстрації завершена"
            )


    # =========================================================================
    # SHOW USER
    # =========================================================================

    @log_errors
    def show_user(
        service,
        email
    ):

        print(
            "\nПошук користувача..."
        )

        try:

            user = service.find_by_email(
                email
            )

            if user is None:

                raise UserError(
                    f"Користувача "
                    f"{email} не знайдено"
                )


        except UserError as error:

            print(
                f"Помилка: {error}"
            )


        else:

            print(
                f"Знайдено: {user}"
            )


        finally:

            print(
                "Пошук завершено"
            )


    # =========================================================================
    # DELETE USER
    # =========================================================================

    @log_errors
    def delete_user(
        service,
        email
    ):

        print(
            "\nВидалення користувача..."
        )

        try:

            user = service.remove_user(
                email
            )


        except UserError as error:

            print(
                f"Помилка: {error}"
            )


        else:

            print(
                f"Користувача "
                f"{user} видалено"
            )


        finally:

            print(
                "Операція видалення завершена"
            )


    # =========================================================================
    # СТВОРЮЄМО SERVICE
    # =========================================================================

    service = UserService()


    # =========================================================================
    # ТЕСТ 1 — КОРЕКТНИЙ КОРИСТУВАЧ
    # =========================================================================

    register_user(
        service,
        "bob_123",
        "bob@gmail.com",
        25,
        "Python12345"
    )


    # =========================================================================
    # ТЕСТ 2 — НЕПРАВИЛЬНИЙ USERNAME
    # =========================================================================

    register_user(
        service,
        "bo",
        "bob2@gmail.com",
        25,
        "Python12345"
    )


    # =========================================================================
    # ТЕСТ 3 — НЕПРАВИЛЬНИЙ EMAIL
    # =========================================================================

    register_user(
        service,
        "john",
        "john@gmail",
        25,
        "Python12345"
    )


    # =========================================================================
    # ТЕСТ 4 — ВІК МЕНШЕ 18
    # =========================================================================

    register_user(
        service,
        "mike",
        "mike@gmail.com",
        15,
        "Python12345"
    )


    # =========================================================================
    # ТЕСТ 5 — НЕПРАВИЛЬНИЙ PASSWORD
    # =========================================================================

    register_user(
        service,
        "mike",
        "mike@gmail.com",
        25,
        "123456789P"
    )


    # =========================================================================
    # ТЕСТ 6 — КОРЕКТНИЙ КОРИСТУВАЧ
    # =========================================================================

    register_user(
        service,
        "mike",
        "mike@gmail.com",
        25,
        "Python12345"
    )


    # =========================================================================
    # ТЕСТ 7 — ДУБЛІКАТ EMAIL
    # =========================================================================

    register_user(
        service,
        "second_bob",
        "bob@gmail.com",
        25,
        "Python12345"
    )


    # =========================================================================
    # ПОШУК ІСНУЮЧОГО КОРИСТУВАЧА
    # =========================================================================

    show_user(
        service,
        "bob@gmail.com"
    )


    # =========================================================================
    # ПОШУК НЕІСНУЮЧОГО КОРИСТУВАЧА
    # =========================================================================

    show_user(
        service,
        "unknown@gmail.com"
    )


    # =========================================================================
    # ВСІ КОРИСТУВАЧІ
    # =========================================================================

    print(
        "\n"
        + "=" * 50
    )

    print(
        "ВСІ КОРИСТУВАЧІ"
    )

    print(
        "=" * 50
    )


    for user in service.get_all_users():

        print(user)


    # =========================================================================
    # ВИДАЛЕННЯ КОРИСТУВАЧА
    # =========================================================================

    delete_user(
        service,
        "mike@gmail.com"
    )


    # =========================================================================
    # СПРОБА ВИДАЛИТИ НЕІСНУЮЧОГО
    # =========================================================================

    delete_user(
        service,
        "mike@gmail.com"
    )


    # =========================================================================
    # КОРИСТУВАЧІ ПІСЛЯ ВИДАЛЕННЯ
    # =========================================================================

    print(
        "\n"
        + "=" * 50
    )

    print(
        "ВСІ КОРИСТУВАЧІ "
        "ПІСЛЯ ВИДАЛЕННЯ"
    )

    print(
        "=" * 50
    )


    for user in service.get_all_users():

        print(user)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # Базові приклади exception
    # -------------------------------------------------------------------------

    example_without_exception()
    example_try_except()
    example_try_except_else_finally()
    example_raise()
    example_assert()
    example_exception_propagation()

    # -------------------------------------------------------------------------
    # Власні exception
    # -------------------------------------------------------------------------

    example_custom_exception()
    example_exception_hierarchy()

    # -------------------------------------------------------------------------
    # Decorator + exception
    # -------------------------------------------------------------------------

    example_log_errors()

    # -------------------------------------------------------------------------
    # Regex
    # -------------------------------------------------------------------------

    example_regex_username()
    example_regex_email()
    example_regex_password()

    # -------------------------------------------------------------------------
    # Classes
    # -------------------------------------------------------------------------

    example_user_class()
    example_user_service()

    # -------------------------------------------------------------------------
    # Фінальний мініпроєкт
    # -------------------------------------------------------------------------

    example_final_project()