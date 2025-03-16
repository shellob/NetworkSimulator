import time
from World import World
from ConfigParser import ConfigParser
from Message import Message


def echo_function(message: Message):
    print(f"✅ [Эхо] Процесс {message.receiver_id} получил: {message.data.decode('utf-8')}")  # 🔥 Должно появляться




def main():
    world = World()
    parser = ConfigParser(world)

    try:
        parser.parse("config.txt")
    except Exception as e:
        print(f"⚠️ Ошибка при загрузке конфигурации: {e}")
        return

    for process_id, process in world.processes.items():
        if not process.has_function("echo"):
            print(f"Добавляем функцию 'echo' в процесс {process_id}")
            process.add_function("echo", echo_function)

    world.start_all_processes()

    time.sleep(5)  # Даем симуляции время на обработку сообщений

    world.stop_all_processes()


if __name__ == "__main__":
    main()
