from World import World
from Message import Message


class ConfigParser:
    def __init__(self, world: World):
        self.world = world
        self.bidirected = True

    def parse(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue
                    self._parse_command(line)
        except FileNotFoundError:
            print(f"⚠️ Ошибка: Файл {filepath} не найден!")
        except Exception as e:
            print(f"⚠️ Ошибка при чтении конфигурации: {e}")

    def _parse_range(self, start: str, end: str):
        try:
            return range(int(start), int(end) + 1)
        except ValueError:
            print(f"⚠️ Ошибка: Неверный формат чисел в диапазоне {start}-{end}")
            return range(0)

    def _parse_link(self, parts: list[str]):
        try:
            if parts[1] == 'from' and parts[2] == 'all' and parts[3] == 'to' and parts[4] == 'all':
                process_ids = list(self.world.processes.keys())
                for from_id in process_ids:
                    for to_id in process_ids:
                        if from_id != to_id:
                            self.world.network.create_channel(from_id, to_id, latency=0, bidirected=self.bidirected)
            else:
                from_id = int(parts[2])
                to_id = int(parts[4])
                latency = float(parts[6])
                self.world.network.create_channel(from_id, to_id, latency, bidirected=self.bidirected)
        except (IndexError, ValueError):
            print(f"⚠️ Ошибка: Неверный формат команды link {' '.join(parts)}")

    def _parse_command(self, line: str):
        parts = line.split()
        if not parts:
            return

        cmd = parts[0]

        try:
            if cmd == 'processes':
                m, n = int(parts[1]), int(parts[2])
                self.world.create_processes_range(m, n)



            elif cmd == 'setprocesses':
                m, n, algorithm_name = int(parts[1]), int(parts[2]), parts[3]
                def echo_function(msg: Message):
                    print(f"✅ [Эхо] Процесс {msg.receiver_id} получил: {msg.data.decode('utf-8')}")
                for pid in range(m, n + 1):
                    if pid in self.world.processes:
                        print(f"🔧 Назначаем процессу {pid} алгоритм '{algorithm_name}'")
                        self.world.assign_function_to_process(pid, algorithm_name, echo_function)


            elif cmd == 'link':
                self._parse_link(parts)

            elif cmd == 'send':
                from_id = int(parts[2])
                to_id = int(parts[4])
                message_text = ' '.join(parts[5:]).encode('utf-8')
                msg = Message(from_id, to_id, data=message_text, algorithm="echo")
                print(f"📤 Отправка сообщения: {msg}")
                self.world.network.send_message(msg)

            elif cmd == 'bidirected':
                self.bidirected = bool(int(parts[1]))

            else:
                print(f"⚠️ Неизвестная команда: {cmd}")

        except (IndexError, ValueError):
            print(f"⚠️ Ошибка: Неверный формат команды {cmd} {' '.join(parts)}")

    def __repr__(self):
        return f"<ConfigParser bidirected={self.bidirected}>"
