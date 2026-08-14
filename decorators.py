# def handle_get(request):
#     return "GET Response"
#
# def handle_post(request):
#     return "POST Response"
#
# routers = {
#     "GET": handle_get,
#     "POST": handle_post
# }
#
# def process_request(method, request):
#     handler = routers.get(method)
#     if handler:
#         return handler(request)
#
#     return "405 Method Not Allowed"
#
# print(process_request("PUT", {}))

# import functools
#
# def error(message):
#     print(f"[ERROR] {message}")
#
# def info(message):
#     print(f"[INFO] {message}")
#
# def error_handler_factory(func_error):
#     def error_handler(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 func_error(f"Error in {func.__name__}: {e}")
#                 return None
#         return wrapper
#     return error_handler
#
# handle_error = error_handler_factory(error)
# handle_info = error_handler_factory(info)
#
# @error_handler_factory(error)
# def process_order(order):
#     if order.get("amount", 0) <= 0:
#         raise ValueError("Amount <= 0")
#
#     return "Order processed"
#
# order1 = {"amount": 0}
# print(process_order(order1))


# def decorator_hello(func):
#     def wrapper():
#         print("Before print Hello")
#         func()
#         return 5+5
#     return wrapper
#
# @decorator_hello
# def hello():
#     print("Hello")
#
# print(hello())
import time
#
# def decorator_add(func):
#     def wrapper(*args, **kwargs):
#         print(f"Function {func.__name__} start")
#         result = func(*args, **kwargs)
#         print(f"Function {func.__name__} end")
#         return result
#     return wrapper
#
# def timer(func):
#     def wrapper(*args, **kwargs):
#         print(f"START {func.__name__}".upper().center(100, "="))
#         start = time.time()
#         result = func(*args, **kwargs)
#         print(f"Result {func.__name__} = {result}")
#         end = time.time()
#         print(f"Function {func.__name__} processing time: {end - start}s")
#         print("=" * 100 + '\n')
#         return result
#     return wrapper
#
# @timer
# def add(a, b):
#     return a+b
#
# @timer
# def multiply(a, b):
#     return a*b
# @timer
# def power(x):
#     time.sleep(1)
#     return x**100
#
# res_add = add(5, 5)
# multiply(5, 5)
# power(5)
# print(res_add)


# def count_calls(func):
#     count = 0
#     def wrapper(*args, **kwargs):
#         nonlocal count
#         count += 1
#         if count % 3 == 0:
#             print("Wait 1 seconds")
#             time.sleep(1)
#         print(f"Function {func.__name__} called with {count} calls")
#         return func(*args, **kwargs)
#     return wrapper
#
# def repeat(times):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             for _ in range(times):
#                 func(*args, **kwargs)
#         return wrapper
#     return decorator
#
# @repeat(10)
# def hello():
#     print("Hello World")
#
# hello()
from functools import wraps
#
# def admin_only(func):
#     @wraps(func)
#     def wrapper(user, *args, **kwargs):
#         if user != "admin":
#             print("403 Forbidden")
#             return
#         return func(user, *args, **kwargs)
#     return wrapper
#
# @admin_only
# def delete_user(user, username):
#     """Delete user by username"""
#     print(f"{user} deleted {username}")
#
# # delete_user("role_user", "admin")
# # delete_user("admin", "role_user")
# print(delete_user.__doc__)
# print(delete_user.__name__)

# def cache(func):
#     storage = {}
#     @wraps(func)
#     def wrapper(*args):
#         if args in storage:
#             print("Cache hit")
#             return storage[args]
#         print("Calculate...")
#         result = func(*args)
#         storage[args] = result
#         return result
#     return wrapper
#
# @cache
# def calculate(number):
#     time.sleep(2)
#     return number * 10
#
# start = time.time()
# print(calculate(5))
# print(calculate(5))
# print(calculate(5))
# print(calculate(2))
# print(calculate(5))
# print(calculate(2))
# end = time.time()
# print(f"Calculate processed {end - start}s")

import re

# def validate_email(func):
#     @wraps(func)
#     def wrapper(email, *args, **kwargs):
#         pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
#
#         if not re.fullmatch(pattern, email):
#             raise ValueError(f"Invalid email: {email}")
#
#         return func(email, *args, **kwargs)
#     return wrapper
#
# @validate_email
# def register(email):
#     print(f"User {email} registered")
#
# register("user@gmail.com")


# def regex_validate(pattern):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(value, *args, **kwargs):
#             if not re.fullmatch(pattern, value):
#                 raise ValueError(f"Invalid {value} doesnt match {pattern}")
#             return func(value, *args, **kwargs)
#         return wrapper
#     return decorator
#
#
# @regex_validate(r"\+380\d{9}")
# def save_phone(value):
#     print(f"{value} Saved")
#
# # save_phone("+380991234567")
# # save_phone("0991234567")
#
# @regex_validate(r"\d{4}")
# def enter_pin(value):
#     print("Correct PIN")
#
# enter_pin("1234")

# def parse_user(func):
#     @wraps(func)
#     def wrapper(text):
#         pattern = r"User:\s*(?P<name>[\w]+),\s*Age:\s*(?P<age>\d+)"
#
#         match = re.fullmatch(pattern, text)
#         if not match:
#             raise ValueError
#
#         data = match.groupdict()
#         return func(**data)
#     return wrapper
#
# @parse_user
# def create_user(name, age):
#     print(f"Name: {name}")
#     print(f"Age: {age}")
#
# create_user("User: Bob, Age: 30")

# def mask_card(func):
#     @wraps(func)
#     def wrapper(card, *args, **kwargs):
#         masked = re.sub(
#             r"\d{4}\s*\d{4}\s*\d{4}\s*(\d{4})",
#             r"**** **** **** \1",
#             card
#         )
#         return func(masked, *args, **kwargs)
#     return wrapper
#
# @mask_card
# def enter_card(card):
#     print(f"Card: {card}")
#
# enter_card("1234 5678 9012 3456")

# def clean_text(func):
#     @wraps(func)
#     def wrapper(text, *args, **kwargs):
#         text = re.sub(
#             r'<[^>]+>',
#             "",
#             text
#         )
#
#         text = re.sub(
#             r"\s+",
#             " ",
#             text
#         )
#
#         text = text.strip()
#
#         return func(text, *args, **kwargs)
#
#     return wrapper
# @clean_text
# def save_description(text):
#     print(repr(text))
#
# save_description(
#     "<p>Hello</p>   <b>world</b>\n\n           Python     "
# )



# def validate(**patterns):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(**kwargs):
#             for name, pattern in patterns.items():
#                 value = kwargs.get(name)
#
#                 if value is None:
#                     continue
#
#                 if not re.fullmatch(pattern, value):
#                     raise ValueError(f"{name}={value} doesn't match {pattern}")
#
#             return func(**kwargs)
#         return wrapper
#     return decorator
#
#
# @validate(
#     username=r"[a-zA-Z0-9_-]{3,20}",
#     email=r"^[\w.-]+@[\w.-]+\.\w+$",
#     phone=r'\+380\d{9}'
# )
# def register(username, email, phone):
#     print(f"Registered: {username}")
#
# register(
#     username="bob_user",
#     email="bob@gmail.com",
#     phone="+380123456789"
# )


def type_check(**types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect

            signature = inspect.signature(func)
            bound = signature.bind(*args, **kwargs)

            for name, value in bound.arguments.items():
                if name not in types:
                    continue

                expected_type = types[name]

                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"{name} must be {expected_type.__name__}, but got {type(value).__name__}"
                    )

            return func(*args, **kwargs)
        return wrapper
    return decorator


@type_check(
    name=str,
    age=int,
    price=float
)
def create_product(name, age, price):
    print(name, age, price)

create_product(
    "iPhone",
    10,
    999.99
)