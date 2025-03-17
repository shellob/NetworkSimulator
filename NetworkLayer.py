import time
from typing import Dict, Tuple, List
from Message import Message
from MessageQueue import MessageQueue


class NetworkLayer:
    def __init__(self):
        self.channels: Dict[Tuple[int, int], Dict[str, float]] = {}
        self.message_queues: Dict[int, MessageQueue] = {}
        self.global_time = time.time()

    def create_channel(self, from_id: int, to_id: int, latency: float, bidirected: bool = True):
        if (from_id, to_id) in self.channels:
            print(f"⚠️ Канал между {from_id} и {to_id} уже существует!")
            return

        self.channels[(from_id, to_id)] = {'latency': latency}
        if bidirected:
            self.channels[(to_id, from_id)] = {'latency': latency}

    def add_channel_to_map(self, from_id: int, to_id: int, properties: dict):
        self.channels[(from_id, to_id)] = properties

    def get_channel_properties(self, from_id: int, to_id: int):
        return self.channels.get((from_id, to_id), None)

    def create_message_queue(self, process_id: int):
        if process_id in self.message_queues:
            print(f"⚠️ Очередь сообщений для процесса {process_id} уже существует!")
            return
        self.message_queues[process_id] = MessageQueue()
        print(f"✅ Создана очередь сообщений для процесса {process_id}")

    def get_message_queue(self, process_id: int) -> MessageQueue:
        if process_id not in self.message_queues:
            print(f"⚠️ Очередь сообщений для процесса {process_id} не найдена, создаём новую!")
            self.message_queues[process_id] = MessageQueue()
        return self.message_queues[process_id]

    def send_message(self, message: Message):
        channel = self.get_channel_properties(message.sender_id, message.receiver_id)
        if channel:
            latency = channel.get('latency', 0)
            time.sleep(latency)

            queue = self.get_message_queue(message.receiver_id)
            print(f" Сообщение добавлено в очередь {message.receiver_id}: {message}")
            queue.add_message(priority=int(time.time()), message=message)
        else:
            print(f" Ошибка: Канал {message.sender_id} → {message.receiver_id} не существует!")

    def get_neighbors(self, node_id: int) -> List[int]:
        return [to_id for (from_id, to_id) in self.channels.keys() if from_id == node_id]

    def __repr__(self):
        return f"<NetworkLayer nodes={len(self.message_queues)}, channels={len(self.channels)}>"
