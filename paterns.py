# class CityHall:
#     _instance = None
#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             print("Create single city hall")
#             # cls._instance = super().__new__(cls, *args, **kwargs)
#
#         return cls._instance
#
#     def serve_citizen(self):
#         print("serve citizen")
from abc import ABC, abstractmethod
from turtle import TNavigator


# cityhall1 = CityHall()
# cityhall2 = CityHall()
# cityhall3 = CityHall()
# cityhall1.serve_citizen()
# cityhall2.serve_citizen()
# cityhall3.serve_citizen()
# print(cityhall1 is cityhall2)
# print(cityhall1 is cityhall3)

# import threading
#
# class DBConnection:
#     _instance = None
#     _lock = threading.Lock()
#
#     def __new__(cls, *args, **kwargs):
#         with cls._lock:
#             if cls._instance is None:
#                 cls._instance = super().__new__(cls, *args, **kwargs)
#                 cls._instance.connect()
#             return cls._instance
#
#     def connect(self):
#         print("Connection to DB")
#
#
# db1 = DBConnection()
# db2 = DBConnection()
#
# db1.connect()
# print(db1 is db2)

# from abc import ABC, abstractmethod
#
# class Toy(ABC):
#     @abstractmethod
#     def play(self):
#         pass
#
# class Ball(Toy):
#     def play(self):
#         print("Play with Ball")
#
#     def hello(self):
#         print("hello ball")
#
# class Bear(Toy):
#     def play(self):
#         print("Play with Bear")
#
# class Car(Toy):
#     def play(self):
#         print("Play with Car")
#
# ball = Ball()
# car = Car()
# bear = Bear()
#
# ball.play()
# car.play()
# bear.play()


# class Notification:
#     def send(self, message):
#         print(f"Send notification {message}")
#
# class EmailNotification(Notification):
#     def send(self, message):
#         print(f"Send email notification {message}")
#
# class SMSNotification(Notification):
#     def send(self, message):
#         print(f"Send sms notification {message}")
#
# class TelegramNotification(Notification):
#     def send(self, message):
#         print(f"Send telegram notification {message}")
#
#
# class NotificationFactory:
#     @staticmethod
#     def create_notification(method):
#         if method == "email":
#             return EmailNotification()
#         elif method == "sms":
#             return SMSNotification()
#         elif method == "telegram":
#             return TelegramNotification()
#         else:
#             return Notification()
#
#
# NotificationFactory.create_notification("sms").send("Hello")
# NotificationFactory.create_notification("email").send("Hello")
# NotificationFactory.create_notification("telegram").send("Hello")



# class SocialMediaAccount:
#     def __init__(self, username):
#         self.username = username
#         self.followers = []
#
#     def subscribe(self, observer):
#         self.followers.append(observer)
#
#     def unsubscribe(self, observer):
#         self.followers.remove(observer)
#
#     def new_post(self, content):
#         print(f"{self.username}: !!!NEW POST!!! {content}")
#         self.notify_followers(content)
#
#     def notify_followers(self, content):
#         for follower in self.followers:
#             follower.update(self, content)
#
# class Follower:
#     def __init__(self, name):
#         self.name = name
#
#     def update(self, account, content):
#         print(f"{self.name}: !!!GET NOTIFICATION!!! {account.username} - {content}")
#
# account = SocialMediaAccount("Popular_Olga")
# follower1 = Follower("Ivan")
# follower2 = Follower("Bob")
#
# account.subscribe(follower1)
# account.subscribe(follower2)
#
# account.new_post("Hello world!")
#
# account.unsubscribe(follower1)
#
# account.new_post("Hi Hi Hi I'm here")
#
#
# account.unsubscribe(follower2)
# account.new_post("Hello world 2!")

# class Coffe(ABC):
#     @abstractmethod
#     def get_cost(self):
#         pass
#
#     @abstractmethod
#     def get_description(self):
#         pass
#
#
# class SimpleCoffe(Coffe):
#     def get_cost(self):
#         return 50
#
#     def get_description(self):
#         return "Simple Coffe"
#
# class CoffeeDecorator(Coffe):
#     def __init__(self, decorator_coffee: Coffe):
#         self.decorator_coffe = decorator_coffee
#
#     def get_cost(self):
#         return self.decorator_coffe.get_cost()
#
#     def get_description(self):
#         return self.decorator_coffe.get_description()
#
# class MilkDecorator(CoffeeDecorator):
#     def get_cost(self):
#         print("Milk Add Cost: (+10)")
#         return self.decorator_coffe.get_cost() + 10
#
#     def get_description(self):
#         return self.decorator_coffe.get_description() + " with Milk"
#
#
# class SugarDecorator(CoffeeDecorator):
#     def get_cost(self):
#         return self.decorator_coffe.get_cost() + 5
#
#     def get_description(self):
#         return self.decorator_coffe.get_description() + " with sugar"
#
#
# basic_coffe = SimpleCoffe()
# print(basic_coffe.get_cost())
# print(basic_coffe.get_description())
# basic_coffe = MilkDecorator(basic_coffe)
# # basic_coffe = SugarDecorator(basic_coffe)
# # basic_coffe = MilkDecorator(basic_coffe)
# # basic_coffe = SugarDecorator(basic_coffe)
# print(basic_coffe.get_cost())
# print(basic_coffe.get_description())


# class ExternalDevice:
#     def plug_in(self):
#         print("Device connect with help plug_in")
#
# class DeviceInterface:
#     def connect(self):
#         raise NotImplementedError()
#
#
# class DeviceAdapter(DeviceInterface):
#     def __init__(self, external_device: ExternalDevice):
#         self.external_device = external_device
#
#     def connect(self):
#         self.external_device.plug_in()
#
#
# external_device1 = ExternalDevice()
# device_interface = DeviceInterface()
# # device_interface.connect()
# adapter = DeviceAdapter(external_device1)
# adapter.connect()

# class API:
#     def get_usd_rate(self):
#         # return 40
#         raise NotImplementedError
#
# class ExternalCurrencyAPI:
#     def get_rate(self):
#         return {"usd": 40, "eur": 42}
#
# class CurrencyAdapter:
#     def __init__(self, api):
#         self.api = api
#
#     def get_usd_rate(self):
#         return self.api.get_rate()["usd"]
#
#
#
#
#
# # api = API()
# api = ExternalCurrencyAPI()
# adapter = CurrencyAdapter(api)
# api = adapter
# print(api.get_usd_rate())


# class RouteStrategy(ABC):
#     @abstractmethod
#     def get_route(self, start, end):
#         pass
#
# class FastRoute(RouteStrategy):
#     def get_route(self, start, end):
#         return f"Fast Route {start} -> {end}"
#
# class SlowRoute(RouteStrategy):
#     def get_route(self, start, end):
#         return f"Slow Route {start} -> {end}"
#
# class Navigator:
#     def __init__(self, strategy: RouteStrategy):
#         self.strategy = strategy
#
#     def set_strategy(self, strategy: RouteStrategy):
#         self.strategy = strategy
#
#     def navigate(self, start, end):
#         route = self.strategy.get_route(start, end)
#         print(route)
#
# navigator = Navigator(FastRoute())
# navigator.navigate("A", "B")
#
# print("Oooops some problem on fast route")
# navigator.set_strategy(SlowRoute())
# navigator.navigate("A", "B")


# class Command(ABC):
#     @abstractmethod
#     def execute(self):
#         pass
#
# class TV:
#     def __init__(self, name):
#         self.name = name
#
#     def on(self):
#         print(f"TV is on {self.name}")
#
#     def off(self):
#         print(f"TV is off {self.name}")
#
#
# class TVOnCommand(TV):
#     def __init__(self, tv: TV):
#         self.tv = tv
#
#     def execute(self):
#         self.tv.on()
#
#
# class TVOffCommand(TV):
#     def __init__(self, tv: TV):
#         self.tv = tv
#
#     def execute(self):
#         self.tv.off()
#
# class RemoteControl:
#     def __init__(self):
#         self.commands = {}
#
#     def add_command(self, num_btn, command):
#         self.commands[num_btn] = command
#
#     def press_btn(self, num_btn):
#         return self.commands[num_btn].execute()
#
# tv = TV("Samsung")
# tv2 = TV("Sony")
# remote = RemoteControl()
# remote.add_command(1, TVOnCommand(tv))
# remote.add_command(2, TVOffCommand(tv))
# remote.add_command(3, TVOnCommand(tv2))
# remote.add_command(4, TVOffCommand(tv2))
#
# while True:
#     print(f"Press 1 for Samsung is on")
#     print(f"Press 2 for Samsung is off")
#     print(f"Press 3 for Sony is on")
#     print(f"Press 4 for Sony is off")
#     print(f"Press 0 for exit")
#     choice = int(input(f"Your choice: "))
#
#     if choice != 0:
#         remote.press_btn(choice)
#     else:
#         break


# class TrafficLightState(ABC):
#     @abstractmethod
#     def handle(self, traffic_light):
#         pass
#
# class RedState(TrafficLightState):
#     def handle(self, traffic_light):
#         print("Traffic light state is red - STOP!")
#         traffic_light.state = YellowState()
#
# class YellowState(TrafficLightState):
#     def handle(self, traffic_light):
#         print("Traffic light state is yellow - STEADY!")
#         traffic_light.state = GreenState()
#
#
# class GreenState(TrafficLightState):
#     def handle(self, traffic_light):
#         print("Traffic light state is green - GO!")
#         traffic_light.state = RedState()
#
# class TrafficLight:
#     def __init__(self):
#         self.state: TrafficLightState = RedState()
#
#     def change(self):
#         self.state.handle(self)
#
#
# light = TrafficLight()
# for _ in range(11):
#     light.change()

#
# class Kitchen:
#     def __init__(self):
#         self.orders = {}
#
#     def add_order(self, table, order):
#         self.orders[table] = order
#         print(f"[Kitchen]: Take order {order} - table {table}")
#
#     def get_order(self, table):
#         return self.orders.get(table, "Can't find order")
#
# class DiningRoom:
#     def bring_order(self, table, order):
#         print(f"[Dining Room]: Table {table} get order {order}")
#
# class Waiter:
#     def __init__(self, kitchen: Kitchen, dining_room: DiningRoom):
#         self.kitchen = kitchen
#         self.dining_room = dining_room
#
#     def take_order(self, table, order):
#         print(f"[Waiter]: Take order {order} - table {table}")
#         self.kitchen.add_order(table, order)
#
#     def serve_order(self, table):
#         order = self.kitchen.get_order(table)
#         self.dining_room.bring_order(table, order)
#
#
# kitchen = Kitchen()
# dining_room = DiningRoom()
# waiter = Waiter(kitchen, dining_room)
# waiter.take_order(5, "Pizza")
# waiter.take_order(1, "Soup")
# waiter.serve_order(1)
# waiter.serve_order(5)


class FileSystemComponent(ABC):
    @abstractmethod
    def show_info(self):
        pass

class File(FileSystemComponent):
    def __init__(self, file_name):
        self._file_name = file_name

    def show_info(self, indent = 0):
        print(" " * indent + f"[File]: {self._file_name}")

class Folder(FileSystemComponent):
    def __init__(self, folder_name):
        self._folder_name = folder_name
        self.children = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def show_info(self, indent = 0):
        print(" " * indent + f"[Folder]: {self._folder_name}")
        for child in self.children:
            child.show_info(indent = 2)

main_folder = Folder("main_folder")
docs_folder = Folder("docs_folder")
media_folder = Folder("media_folder")
excel_folder = Folder("excel_folder")
csv_folder = Folder("csv_folder")

file_csv1 = File("file_csv1.csv")
file_csv2 = File("file_csv2.csv")
file_excel1 = File("file_excel1.xlsx")
file_jpg1 = File("file_jpg1.jpg")

main_folder.add(docs_folder)
main_folder.add(main_folder)

docs_folder.add(csv_folder)
docs_folder.add(excel_folder)

csv_folder.add(file_csv1)
csv_folder.add(file_csv2)
excel_folder.add(file_excel1)

media_folder.add(file_jpg1)


csv_folder.show_info()
print("="*50)
file_csv1.show_info()
print("="*50)
# main_folder.show_info()




