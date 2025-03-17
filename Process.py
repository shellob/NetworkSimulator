import threading
import time
from typing import Callable, Dict
from Message import Message
from MessageQueue import MessageQueue


class Process(threading.Thread):
    def __init__(self, process_id: int, message_queue: MessageQueue):
        super().__init__()
        self.process_id = process_id
        self.message_queue = message_queue
        self.functions: Dict[str, Callable[[Message], None]] = {}
        self._running = True
        print(f" Процесс {self.process_id} получил очередь сообщений: {self.message_queue}")

    def add_function(self, name: str, func: Callable[[Message], None]):
        if name in self.functions:
            print(f" Функция '{name}' уже назначена процессу {self.process_id}!")
            return
        self.functions[name] = func
        print(f" Функция '{name}' добавлена в процесс {self.process_id}")

    def has_function(self, name: str) -> bool:
        result = name in self.functions
        print(f" Проверка: у процесса {self.process_id} есть функция '{name}'? {'Да' if result else 'Нет'}")
        return result

    def execute_function(self, message: Message):
        func_name = message.algorithm or "echo"
        if self.has_function(func_name):
            print(
                f" Процесс {self.process_id} выполняет {func_name} для сообщения: {message}")
            self.functions[func_name](message)
        else:
            print(f" Процесс {self.process_id}: Функция '{func_name}' не найдена!")

    def run(self):
        print(f" Процесс {self.process_id} запущен!")
        while self._running:
            print(f" Процесс {self.process_id} ждёт сообщение...")
            message = self.message_queue.get_message()

            if message:
                print(f" Процесс {self.process_id} получил сообщение: {message}")
                self.execute_function(message)
            elif self.message_queue.is_empty():
                print(f" Процесс {self.process_id} завершает работу, так как сообщений больше нет.")
                break
            else:
                time.sleep(0.1)

    def stop(self):
        print(f" Остановка процесса {self.process_id}...")
        self._running = False
        self.join()

    def __repr__(self):
        return f"<Process id={self.process_id}, functions={list(self.functions.keys())}>"
