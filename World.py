from typing import Callable, Dict
from Process import Process
from NetworkLayer import NetworkLayer
from Message import Message



class World:
    def __init__(self):
        self.processes: Dict[int, Process] = {}
        self.process_functions: Dict[int, str] = {}
        self.network = NetworkLayer()

    def create_process(self, process_id: int):
        if process_id in self.processes:
            print(f"⚠️ Процесс {process_id} уже существует!")
            return

        message_queue = self.network.get_message_queue(process_id)
        process = Process(process_id, message_queue)
        self.processes[process_id] = process
        print(f"✅ Создан процесс {process_id} с очередью {message_queue}")

    def assign_function_to_process(self, process_id: int, function_name: str, func: Callable[[Message], None]):
        process = self.processes.get(process_id)
        if process:
            process.add_function(function_name, func)
            self.process_functions[process_id] = function_name
            print(f"🔧 Процесс {process_id} получил функцию '{function_name}'")
        else:
            print(f"⚠️ Ошибка: Процесс {process_id} не найден!")

    def assign_function_to_range(self, start_id: int, end_id: int, function_name: str, func: Callable[[Message], None]):
        for pid in range(start_id, end_id + 1):
            self.assign_function_to_process(pid, function_name, func)

    def create_processes_range(self, start_id: int, end_id: int):
        for pid in range(start_id, end_id + 1):
            self.create_process(pid)

    def send_message(self, sender_id: int, receiver_id: int, data: bytes, algorithm: str):
        if sender_id not in self.processes or receiver_id not in self.processes:
            print(f"⚠️ Ошибка: Один из процессов {sender_id} → {receiver_id} не существует!")
            return

        message = Message(sender_id, receiver_id, data, algorithm)
        self.network.send_message(message)
        print(f"📤 Сообщение отправлено: {message}")

    def start_all_processes(self):
        for process in self.processes.values():
            process.start()
            print(f"🚀 Процесс {process.process_id} запущен!")

    def stop_all_processes(self):
        for process in self.processes.values():
            process.stop()
            print(f"🛑 Процесс {process.process_id} остановлен!")

    def __repr__(self):
        return f"<World processes={len(self.processes)}, network_nodes={len(self.network.message_queues)}>"
