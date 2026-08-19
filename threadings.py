import threading
import time
import random

# def task(task_id, delay):
#     print(f"Start task {task_id}")
#     time.sleep(delay)
#     print(f"End task {task_id}")
#
# def run_tasks_in_threads():
#     threads = []
#     for i in range(1, 2000):
#         t = threading.Thread(target=task, args=(i, 2))
#         threads.append(t)
#         t.start()
#     for t in threads:
#         t.join()
#
#
# t1 = time.time()
# run_tasks_in_threads()
# # task(1, 2)
# # task(2, 1)
# # task(3, 1)
# t2 = time.time()
# print(f"Time taken: {t2-t1}s")

# import requests
#
# urls = [
#     "https://www.google.com",
#     "https://www.python.org",
#     "https://www.youtube.com",
#     "https://www.udemy.com",
#     "https://www.cnn.com",
#     "https://www.google.com",
#     "https://www.python.org",
#     "https://www.youtube.com",
#     "https://www.udemy.com",
#     "https://www.cnn.com",
# ]
#
# def fetch_data(url):
#     print(f"Fetching data from {url}")
#     response = requests.get(url)
#     print(f"Data: {response.text[:100]}")
#
# def fetch_url_in_thread(urls):
#     threads = []
#     for url in urls:
#         t = threading.Thread(target=fetch_data, args=(url,))
#         threads.append(t)
#         t.start()
#     for t in threads:
#         t.join()

# t1 = time.time()
# fetch_url_in_thread(urls)
# t2 = time.time()
# print(f"Time taken with threads: {t2-t1}s")
# #
# t1 = time.time()
# for url in urls:
#     fetch_data(url)
# t2 = time.time()
# print(f"Time taken without threads: {t2-t1}s")

# def worker(name, delay):
#     print(f"{name} Started")
#     time.sleep(delay)
#     print(f"{name} Finished")
#
# thread1 = threading.Thread(target=worker, args=("Bob", 2))
# thread2 = threading.Thread(target=worker, args=("Tom", 5))
# thread1.start()
# thread2.start()
# print(thread1.is_alive())
# print(thread2.is_alive())
# thread1.join()
# print(thread1.is_alive())
# print(thread2.is_alive())
# thread2.join()
# print(thread1.is_alive())
# print(thread2.is_alive())

event1 = threading.Event()


# def wait_for_event(name):
#     print(f"{name} Waiting for event")
#     event1.wait()
#     print(f"{name} Event!!!")
#     time.sleep(1)
#     print(f"{name} Finished")
#
# def delay_task():
#     print("DELAY TASK!!!!")
#
# timer = threading.Timer(5, delay_task)
# timer.start()
#
# event1.clear()
# threads = []
# for i in range(1, 4):
#     t = threading.Thread(target=wait_for_event, args=(f"Worker-{i}",))
#     threads.append(t)
#     t.start()
#
# print("Running any function...")
# time.sleep(2)
# print("Finished any function")
# event1.set()
# for t in threads:
#     t.join()
# print("All workers finished")
# timer.cancel()


# tickets = 10
# lock = threading.Lock()
#
# def book_ticket(user):
#     global tickets
#     network = random.uniform(0.1, 1)
#     print(f"{user} network {network}s")
#     time.sleep(network)
#     with lock:
#         if tickets > 0:
#             print(f"{user} booked ticket. Tickets left {tickets - 1}")
#             tickets -= 1
#         else:
#             print(f"{user} tried to book a ticket but sold out")
#
# def user_thread(user):
#     while True:
#         with lock:
#             if tickets <= 0:
#                 break
#         book_ticket(user)
#         thinking = random.uniform(0.8, 1.5)
#         # print(f"{user} thinking {thinking}s")
#         time.sleep(thinking)
#
# threads = []
# for i in range(20):
#     t = threading.Thread(target=user_thread, args=(f"User{i}",))
#     threads.append(t)
#     t.start()
# for t in threads:
#     t.join()


condition = threading.Condition()
shared_data = []

def producer():
    global shared_data
    for _ in range(5):
        with condition:
            item = random.randint(1, 100)
            shared_data.append(item)
            print(f"Producer send item {item} info")
            condition.notify()
            time.sleep(random.uniform(0.5, 1.5))

    with condition:
        shared_data.append(None)
        condition.notify()


def consumer():
    global shared_data
    while True:
        with condition:
            while not len(shared_data):
                condition.wait()
            item = shared_data.pop()
            if item is None:
                print("WORK END!!!")
                break

            print(f"Get item - {item}")

pt = threading.Thread(target=producer)
ct = threading.Thread(target=consumer)
pt.start()
ct.start()
pt.join()
ct.join()









