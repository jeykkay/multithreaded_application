import threading
import time
from queue import Queue


class Order:
    def __init__(self, id, processing_time):
        self.id = id
        self.processing_time = processing_time


class Worker:
    def __init__(self, id, max_workers, order_queue):
        self.id = id
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(max_workers)
        self.order_queue = order_queue

    def process_order(self, order):
        with self.semaphore:
            print(f"Worker {self.id} is processing order {order.id}")

        time.sleep(order.processing_time)
        print(f"Worker {self.id} has completed order {order.id}")
        with self.lock:
            self.order_queue.task_done()


class OrderQueue:
    def __init__(self):
        self.queue = Queue()
        self.completed_tasks = 0

    def add_order(self, order):
        self.queue.put(order)

    def task_done(self):
        self.completed_tasks += 1

    def get_completed_tasks(self):
        return self.completed_tasks


order_queue = OrderQueue()
workers = [Worker(1,2, order_queue), Worker(2, 2, order_queue)]

order1 = Order(1, 2)
order2 = Order(2, 3)
order3 = Order(3, 1)

order_queue.add_order(order1)
order_queue.add_order(order2)
order_queue.add_order(order3)

for worker in workers:
    while not order_queue.queue.empty():
        order = order_queue.queue.get()
        worker.process_order(order)

print(f"Completed tasks: {order_queue.get_completed_tasks()}")
