import asyncio
import random
import time
import threading
import requests
import aiohttp
from requests import session


def sync_task(name, delay):
    print(f"[SYNC] {name} start")
    time.sleep(delay)
    print(f"[SYNC] {name} end")
    return f"[SYNC] {name} done"

async def async_task(name, delay):
    print(f"[ASYNC] {name} start")
    await asyncio.sleep(delay)
    return f"[ASYNC] {name} done"

async def example_run():
    result1 = await async_task("Task 1", 1)
    print(result1)
    result2 = await async_task("Task 2", 2)
    print(result2)
    result3 = await async_task("Task 3", 1)
    print(result3)

async def example_gather():
    results = await asyncio.gather(
        async_task("Task 1", 2),
        async_task("Task 2", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
        async_task("Task 3", 2),
    )
    for result in results:
        print(result)

async def create_tasks_example():
    task1 = asyncio.create_task(async_task(name="Task 1", delay=3))
    task2 = asyncio.create_task(async_task(name="Task 2", delay=1))
    task3 = asyncio.create_task(async_task(name="Task 3", delay=2))

    print("Create 3 tasks")

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1)
    print(result2)
    print(result3)

async def fetch_url(session, url, semaphore):
    async with semaphore:
        print(f"Start fetching {url}")
        async with session.get(url) as response:
            result = response.status
            return {
                "url": url,
                "result": result
            }

async def fetch_many_urls():
    urls = [
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://stackoverflow.com",
    ]

    semaphore = asyncio.Semaphore(3)

    async  with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch_url(session, url, semaphore) for url in urls))
        for result in results:
            print(result)

async def dangerous_task(name):
    await asyncio.sleep(0.5)
    if random.random() < 0.2:
        raise ValueError(f"Dangerous task {name}")
    return f"Success {name}"

async def error_handling_example():
    try:
        result = await dangerous_task("Task 1")
        print(result)
    except ValueError as e:
        print(e)

async def gather_error_handling_example():
    results = await asyncio.gather(
        dangerous_task(name="Task 1"),
        dangerous_task(name="Task 2"),
        dangerous_task(name="Task 3"),
        dangerous_task(name="Task 4"),
        return_exceptions=True
    )

    for result in results:
        print(result)

async def producer(queue):
    for i in range(1, 6):
        item = f"Task-{i}"
        await queue.put(item)

        print(f"[Producer] add {item}")

        await asyncio.sleep(0.3)

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"[Consumer] get {item}")
        await asyncio.sleep(0.8)
        print(f"[Consumer] finished {item}")
        queue.task_done()

async def queue_example():
    queue = asyncio.Queue()

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.put(None)
    await consumer_task

async def worker(worker_id, queue):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        print(f"[Worker-{worker_id}] get {item}")

        await asyncio.sleep(random.uniform(0.5, 1.2))

        print(f"[Worker-{worker_id}] finished {item}")
        queue.task_done()

async def multiply_workers_queue_example():
    queue = asyncio.Queue()

    for i in range(1,6):
        print(f"[Producer] add {i}")
        await queue.put(f"Task-{i}")

    workers = [
        asyncio.create_task(
            worker(worker_id, queue)
        )
        for worker_id in range(1, 4)
    ]

    await queue.join()

    for _ in workers:
        await queue.put(None)

    await asyncio.gather(*workers)

async def as_completed_example():
    tasks = [
        asyncio.create_task(async_task("Task1", 3)),
        asyncio.create_task(async_task("Task2", 1)),
        asyncio.create_task(async_task("Task3", 2)),
    ]

    for competed_task in asyncio.as_completed(tasks):
        result = await competed_task
        print(result)

# def task(task_id, delay):
#     print(f"Start task {task_id}")
#     time.sleep(delay)
#     print(f"End task {task_id}")
#
# def run_tasks_in_threads():
#     threads = []
#     for i in range(1, 11):
#         t = threading.Thread(target=task, args=(i, 2))
#         threads.append(t)
#         t.start()
#     for t in threads:
#         t.join()
#
#
# t1 = time.time()
# run_tasks_in_threads()
# t2 = time.time()
# print(f"Time taken: {t2-t1}s")

async def main():
    # await example_run()
    # await example_gather()
    # await create_tasks_example()
    # await fetch_many_urls()
    # await error_handling_example()
    # await gather_error_handling_example()
    # await queue_example()
    # await multiply_workers_queue_example()
    # await as_completed_example()

t1 = time.time()
asyncio.run(main())
t2 = time.time()
print(t2-t1)


# def s_fetch_url(url):
#     print(f"Start fetching {url}")
#     result = requests.get(url).status_code
#     return {
#         "url": url,
#         "result": result
#     }
#
# def s_fetch_many_urls():
#     urls = [
#         "https://google.com",
#         "https://github.com",
#         "https://python.org",
#         "https://stackoverflow.com",
#     ]
#
#     results =  [s_fetch_url(url) for url in urls]
#     for result in results:
#         print(result)
#
# t1 = time.time()
# s_fetch_many_urls()
# t2 = time.time()
# print(t2-t1)

