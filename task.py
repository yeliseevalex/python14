"""
===============================================================================
ПРАКТИЧНЕ ЗАВДАННЯ: «КАВ'ЯРНЯ В ГОДИНИ ПІК»
===============================================================================

МЕТА ЗАВДАННЯ
-------------------------------------------------------------------------------
Створіть багатопоточну програму, яка симулює роботу невеликої кав'ярні.

У кав'ярні одночасно працюють:
    • касир;
    • три баристи;
    • менеджер;
    • фоновий монітор роботи кав'ярні.

Кожен працівник повинен працювати у власному потоці.

Програма повинна продемонструвати використання:

    • Thread + start() / join()
    • Lock
    • Event
    • Condition
    • Timer
    • daemon=True

ВАЖЛИВО:
Не просто використовуйте всі примітиви у коді.
Кожен із них повинен вирішувати конкретну проблему синхронізації.


===============================================================================
1.THREAD — ПРАЦІВНИКИ КАВ'ЯРНІ
===============================================================================

Створіть окремі потоки для:

    • касира;
    • Barista-1;
    • Barista-2;
    • Barista-3;
    • менеджера;
    • монітора.

Кожен потік повинен виконувати свою роботу.

Наприклад:

    [Cashier] Приймаю замовлення...
    [Barista-1] Готую капучино...
    [Barista-2] Очікую на замовлення...
    [Manager] Перевіряю роботу кав'ярні...

Для запуску потоків використовуйте:

    thread.start()

Після завершення основних робочих потоків головний потік програми
повинен дочекатися їх завершення за допомогою:

    thread.join()


===============================================================================
2.LOCK — СПІЛЬНА КАСА
===============================================================================

У кав'ярні є спільна змінна:

    money = 0

Кожне замовлення має свою вартість:

    Капучино   — 7 ₾
    Лате       — 6 ₾
    Американо  — 5 ₾
    Сендвіч    — 10 ₾

Після оплати замовлення необхідно збільшити загальну суму:

    money += price

Уявіть, що в кав'ярні працює декілька касирів і вони можуть
одночасно змінювати money.

Це може призвести до race condition.

Створіть Lock:

    money_lock = threading.Lock()

та функцію:

    def add_money(amount):
        ...

Зміна спільної змінної money повинна відбуватися тільки під захистом Lock.

Наприклад:

    with money_lock:
        money += amount

Таким чином одночасно змінювати касу може тільки один потік.


===============================================================================
3.EVENT — КАВОМАШИНА ГОТОВА
===============================================================================

На початку роботи кавомашина ще не готова.

Усі баристи повинні чекати, поки менеджер її запустить.

Створіть:

    coffee_machine_ready = threading.Event()

Поки кавомашина не готова, баристи повинні чекати:

    [Barista-1] Кавомашина ще не готова. Очікую...
    [Barista-2] Кавомашина ще не готова. Очікую...
    [Barista-3] Кавомашина ще не готова. Очікую...

Для очікування використовуйте:

    coffee_machine_ready.wait()

Менеджер через деякий час запускає кавомашину:

    [Manager] Запускаю кавомашину...
    [Manager] Прогрівання...
    [Manager] Кавомашина готова!

Після цього менеджер повинен виконати:

    coffee_machine_ready.set()

Після виклику set() усі баристи, які очікували на цю подію,
можуть продовжити роботу.

Подумайте, чому тут краще використати Event, а не Lock.


===============================================================================
4.CONDITION — ЧЕРГА ЗАМОВЛЕНЬ
===============================================================================

Створіть спільну чергу замовлень:

    orders = []

Касир є Producer — він створює нові замовлення.

Наприклад:

    [Cashier] Нове замовлення: Капучино
    [Cashier] Нове замовлення: Сендвіч
    [Cashier] Нове замовлення: Лате

Касир додає замовлення до черги.

Після появи нового замовлення він повинен повідомити барист:

    condition.notify()

Баристи є Consumer — вони забирають замовлення з черги
та готують їх:

    [Barista-1] Отримав замовлення: Капучино
    [Barista-1] Готую Капучино...
    [Barista-1] Капучино готове!

Але якщо замовлень немає, баристи не повинні постійно перевіряти
чергу в циклі.

Замість цього вони повинні перейти в режим очікування:

    condition.wait()

Коли касир додасть нове замовлення, він повинен повідомити
одного з очікуючих барист:

    condition.notify()

Логіка роботи повинна бути приблизно такою:

    Отримати Condition
            ↓
       Є замовлення?
        /        \
      НІ          ТАК
      ↓            ↓
    wait()     Взяти замовлення
                   ↓
               Приготувати

Доступ до спільної черги також повинен бути синхронізований.


===============================================================================
5. TIMER — ЗАВЕРШЕННЯ АКЦІЇ
===============================================================================

Менеджер оголошує:

    «Сьогодні діє ранкова знижка.
     Через 10 секунд вона закінчиться!»

Створіть Timer, який через 10 секунд викличе функцію:

    finish_discount()

Після завершення таймера повинно з'явитися повідомлення:

    РАНКОВА ЗНИЖКА ЗАКІНЧИЛАСЯ!

Використайте:

    threading.Timer(...)

ВАЖЛИВО:
Головний потік не повинен зупинятися на 10 секунд.
Касир, баристи та інші потоки повинні продовжувати працювати,
поки Timer очікує свого часу.


===============================================================================
6.DAEMON=True — МОНІТОР КАВ'ЯРНІ
===============================================================================

Створіть окремий потік Monitor, який кожні 2 секунди
виводить поточний стан кав'ярні:

    [Monitor]
    Виручка: 42 ₾
    Замовлень у черзі: 2
    Активних барист: 3

Монітор повинен працювати постійно:

    while True:
        ...
        time.sleep(2)

Але він не повинен заважати завершенню основної програми.

Тому створіть його як daemon-потік:

    monitor = threading.Thread(
        target=monitor_cafe,
        daemon=True
    )

Коли всі основні потоки завершаться, програма повинна завершитися,
навіть якщо Monitor продовжує працювати.


===============================================================================
ЗАВЕРШЕННЯ РОБОТИ
===============================================================================

Після того як касир прийняв усі замовлення, а баристи приготували їх,
основні робочі потоки повинні завершитися.

Програма повинна вивести приблизно:

    =================================
    КАВ'ЯРНЯ ЗАВЕРШИЛА РОБОТУ
    =================================

    Загальна виручка: 73 ₾
    Виконано замовлень: 8
    Баристи завершили роботу.

    До побачення!

Фоновий Monitor не повинен блокувати завершення програми.


===============================================================================
ДОДАТКОВЕ ЗАВДАННЯ
===============================================================================

Ускладніть програму.

Уявіть, що в кав'ярні закінчилися стаканчики.

Баристи більше не можуть готувати напої та повинні чекати,
поки менеджер принесе нову коробку.

Наприклад:

    [Barista-1] Стаканчиків немає. Очікую...
    [Barista-2] Стаканчиків немає. Очікую...

Через деякий час менеджер поповнює запас:

    [Manager] Приніс 20 нових стаканчиків!

Після цього баристи повинні продовжити роботу:

    [Barista-1] Продовжую роботу.
    [Barista-2] Продовжую роботу.

САМОСТІЙНО ВИЗНАЧТЕ:

    Що краще використати для цієї ситуації —
    Event чи Condition?

    Чому саме цей примітив підходить краще?


===============================================================================
ОБОВ'ЯЗКОВІ ПРИМІТИВИ
===============================================================================

    Thread
        → працівники кав'ярні

    start()
        → запуск потоків

    join()
        → очікування завершення основних потоків

    Lock
        → захист спільної каси

    Event
        → очікування готовності кавомашини

    Condition
        → черга замовлень Producer–Consumer

    Timer
        → завершення акції через 10 секунд

    daemon=True
        → фоновий монітор кав'ярні

"""


import threading
import time
import random
from dataclasses import dataclass

@dataclass
class Order:
    name: str
    price: int


orders = []
money = 0
completed_orders = 0

money_lock = threading.Lock()
completed_orders_lock = threading.Lock()

condition = threading.Condition()

coffe_machine_ready = threading.Event()
shutdown_event = threading.Event()


def add_money(amount):
    global money
    with money_lock:
        money += amount
        print(f"[Cashier] add {amount}\nTotal money is {money}")

def increment_completed_orders():
    global completed_orders
    with completed_orders_lock:
        completed_orders += 1

def start_coffe_machine():
    print("\n [Manager] Start coffe machine...")
    time.sleep(3)
    print("[Manager] Prepearing coffe machine...")
    time.sleep(2)
    print("[Manager] Coffe machine ready!\n")
    coffe_machine_ready.set()

def cashier():
    orders_to_create = [
        Order("Капучино", 7),
        Order("Лате", 6),
        Order("Сендвіч", 10),
        Order("Американо", 5),
        Order("Чізкейк", 8),
        Order("Круасан", 5),
        Order("Капучино", 7),
        Order("Лате", 6),
    ]

    print(f"[Cashier] Start take orders\n")

    for order in orders_to_create:
        time.sleep(random.uniform(0.5, 1.5))
        print(f"[Cashier] New order {order.name} - {order.price}\n")

        with condition:
            orders.append(order)
            print(f"[Cashier] Add order\nOrders: {len(orders)}")
            condition.notify()

        add_money(order.price)

    print(f"[Cashier] Finish take orders\n")

def barista(name):
    print(f"[{name}] Waiting for ready coffe machine...")
    coffe_machine_ready.wait()
    print(f"[{name} ready!")

    while True:
        with condition:
            while not orders:
                print(f"[{name}] Orders empty. Waiting...")
                if cashier_finished:
                    print(f"[{name}] End work...")
                    return
                condition.wait()

            order = orders.pop(0)

            print(f"[{name}] Get {order.name}")

        print(f"[{name}] Cooked {order.name}...")
        time.sleep(random.uniform(1, 2))
        print(f"[{name}] {order.name} ready!")
        increment_completed_orders()


def manager():
    start_coffe_machine()


def finished_discount():
    print("="*50)
    print("\nFinished discount...")
    print("=" * 50)


cashier_finished = False
cashier_finished_lock = threading.Lock()

def mark_cashier_finished():
    global cashier_finished
    with cashier_finished_lock:
        cashier_finished = True
    with condition:
        condition.notify_all()

def cashier_worker():
    cashier()
    mark_cashier_finished()

def main():
    cashier_thread = threading.Thread(target=cashier_worker)

    barista_threads = []
    for i in range(1, 4):
        barista_threads.append(threading.Thread(target=barista, args=(f"Barista-{i}",)))

    manager_thread = threading.Thread(target=manager, args=())

    discount_timer = threading.Timer(7, finished_discount)

    print("Start work...")
    manager_thread.start()
    for barista_thread in barista_threads:
        barista_thread.start()

    cashier_thread.start()

    discount_timer.start()

    cashier_thread.join()
    print("[Main] Cashier finished!")

    manager_thread.join()
    print("[Main] Manager finished!")

    for thread in barista_threads:
        thread.join()
    print("[Main] Barista finished!")

    with money_lock:
        final_money = money

    with completed_orders_lock:
        final_completed_orders = completed_orders

    print(f"Final Money is {final_money}")
    print(f"Total completed orders is {final_completed_orders}")
    print("END!")

main()