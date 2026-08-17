# def divide_without_exception(a, b):
#     return a / b
#
# # print(divide_without_exception(1, 0))
#
# def divide_with_exception(a, b):
#     try:
#         return a / b
#     except ZeroDivisionError:
#         print(f"Error ZeroDivisionError")
#         return None
#
# print(divide_with_exception(1, 0))
# print(divide_with_exception(1, 0))
# print(divide_with_exception(1, 0))
# print(divide_with_exception(1, 0))
# print(divide_with_exception(1, 0))
# print(divide_with_exception(1, 2))


# def divide(a, b):
#     try:
#         result = a / b
#     except ZeroDivisionError:
#         print("ERROR: division by zero")
#         return None
#     else:
#         print("Success")
#         return result
#     finally:
#         print("Operation is end")
#
# print(divide(1, 2))


# def check_age(age):
#     if age < 0:
#         raise ValueError("Age must be greater than 0")
#     return age
#
#
# print(check_age(1))
# print(check_age(10))
# print(check_age(-1))
# print(check_age(1))

# def calculate_avg_list(numbers):
#     assert len(numbers) > 0, "numbers must not be empty"
#     return sum(numbers) / len(numbers)
#
# print(calculate_avg_list([]))
# def function_c():
#     # raise KeyError("missing key in  JSON")
#     return 0
# def function_b(n):
#     if n:
#         function_c()
#     raise ValueError("Oops")
#
# def function_a():
#     try:
#         function_b(50)
#     except ValueError:
#         print("Error in function_b")
#
# function_a()

# class AuthenticationError(Exception):
#     def __init__(self, message="Authentication Error"):
#         super().__init__(message)
#
# def authentication_user(username, password):
#     if username != "admin" or password != "12345":
#         raise AuthenticationError("Invalid username or password")
#     return True
#
#
# print(authentication_user("admin", "1234"))


import re
from functools import wraps

class UserError(Exception):
    pass

class ValidationError(UserError):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.message = message
        self.field = field

    def ___str__(self):
        if self.field:
            return f"[{self.field}] {self.message}"
        return self.message

class UserAlreadyExists(UserError):
    pass

class User:
    def __init__(self, username, email, age, password):
        self.username = username
        self.email = email
        self.age = age
        self.password = password

    def __str__(self):
        return f"{self.username} <{self.email}>"

class UserService:
    def __init__(self):
        self.users = []

    def find_by_email(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None

    def add_user(self, user):
        if self.find_by_email(user.email):
            raise UserAlreadyExists("Користувач з таким email вже існує")
        self.users.append(user)

    def remove_user(self, email):
        user = self.find_by_email(email)
        if not user:
            raise UserError("Користувача з таким email не знайдено")
        self.users.remove(user)
        return user

    def get_all_users(self):
        return self.users

def log_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            print(f"[LOG] Помилка: {error}")
            raise
        finally:
            print(f"[LOG] Функція {func.__name__} завершила роботу")

        return result
    return wrapper

def validate_username(username):
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    if not re.fullmatch(pattern, username):
        raise ValidationError("Username повинен містити 3-20 символів та складатися з букв, цифр та _", field="username")

def validate_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
    if not re.fullmatch(pattern, email):
        raise ValidationError("Некоректний email", field="email")

def validate_age(age):
    if age < 18:
        raise ValidationError("Користувач повинен бути старше 18 років", field="age")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Пароль повинен містити мінімум 8 символів", field="password")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Пароль повинен містити хоча б одну велику літеру", field="password")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Пароль повинен містити хоча б одну маленьку літеру", field="password")
    if not re.search(r"\d", password):
        raise ValidationError("Пароль повинен містити хоча б одну цифру", field="password")


@log_errors
def register_user(service, username, email, age, password):
    print('\n' + '=' * 50)
    print("ПОЧАТОК РЕЄСТРАЦІЇ")
    print("=" * 50)

    try:
        validate_username(username)
        validate_email(email)
        validate_age(age)
        validate_password(password)

        user = User(username=username, email=email, age=age, password=password)
        service.add_user(user)

    except ValidationError as error:
        print(f"Помилка валідації: {error}")

    except UserAlreadyExists as error:
        print(error)

    except Exception as error:
        print(f"Невідома помилка: {error}")

    else:
        print(f"Користувача {user.username} успішно зареєстровано!")

    finally:
        print("Операція реєстрації завершена")

@log_errors
def show_user(service, email):
    print("\nПошук користувача...")
    try:
        user = service.find_by_email(email)
        if user is None:
            raise UserError(f"Користувача {email} не знайдено")
    except UserError as error:
        print(f"{error}")
    else:
        print(f"Знайдено: {user}")
    finally:
        print("Пошук завершено")

@log_errors
def delete_user(service, email):
    print("\nВидалення користувача...")
    try:
        user = service.remove_user(email)
    except UserError as error:
        print(f"{error}")
    else:
        print(f"Користувача {user} видалено")
    finally:
        print(f"Операція видалення завершена")


service = UserService()

register_user(service, "bob_123", "bob@gmail.com", 25, "Python12345")
register_user(service, "bo", "bob2@gmail.com", 25, "Python12345")
register_user(service, "john", "john@gmail", 25, "Python12345")
register_user(service, "mike", "mike@gmail.com", 15, "Python12345")
register_user(service, "mike", "mike@gmail.com", 25, "123456789P")
register_user(service, "mike", "mike@gmail.com", 25, "Python12345")
register_user(service, "second_bob", "bob@gmail.com", 25, "Python12345")

show_user(service, "bob@gmail.com")
show_user(service, "bob2@gmail.com")

print('\n' + '=' * 50)
print("ВСІ КОРИСТУВАЧІ")
print("=" * 50)

for user in service.get_all_users():
    print(user)

delete_user(service, "mike@gmail.com")
delete_user(service, "mike2@gmail.com")

print('\n' + '=' * 50)
print("ВСІ КОРИСТУВАЧІ ПІСЛЯ ВИДАЛЕННЯ")
print("=" * 50)

for user in service.get_all_users():
    print(user)



