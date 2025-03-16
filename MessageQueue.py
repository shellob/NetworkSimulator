import threading
from queue import PriorityQueue, Empty
from typing import Optional
from Message import Message


class MessageQueue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.mutex = threading.Lock()

    def add_message(self, priority: int, message: Message):
        with self.mutex:
            self.queue.put((priority, message))
            print(f"📩 Добавлено сообщение в очередь: {message}")

    def get_message(self) -> Optional[Message]:
        with self.mutex:
            try:
                if self.queue.empty():
                    print(f"⚠️ Очередь пуста!")
                    return None
                priority, message = self.queue.get_nowait()
                print(f"📤 Извлекаем сообщение из очереди: {message}")
                return message
            except Empty:
                print(f"⚠️ Ошибка: Очередь была пуста при get_nowait()")
                return None

    def get_size(self) -> int:
        with self.mutex:
            return self.queue.qsize()

    def is_empty(self) -> bool:
        with self.mutex:
            return self.queue.empty()

    def __repr__(self):
        return f"<MessageQueue size={self.get_size()}>"
