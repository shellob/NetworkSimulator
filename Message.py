import json
import time
from datetime import datetime
from typing import Optional


class Message:
    def __init__(
        self,
        sender_id: int,
        receiver_id: int,
        data: bytes,
        algorithm: Optional[str] = None,
        sent_time: Optional[float] = None,
        received_time: Optional[float] = None,
    ):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.data = data if isinstance(data, bytes) else data.encode("utf-8")
        self.algorithm = algorithm
        self.sent_time = sent_time or time.time()
        self.received_time = received_time

    @classmethod
    def from_text(cls, sender_id: int, receiver_id: int, text: str, algorithm: Optional[str] = None):
        return cls(sender_id, receiver_id, text.encode("utf-8"), algorithm)

    @classmethod
    def from_json(cls, sender_id: int, receiver_id: int, obj: dict, algorithm: Optional[str] = None):
        try:
            data_bytes = json.dumps(obj).encode("utf-8")
            return cls(sender_id, receiver_id, data_bytes, algorithm)
        except TypeError:
            print(f"⚠️ Ошибка сериализации JSON: {obj}")
            return cls(sender_id, receiver_id, b"{}", algorithm)

    def deserialize_to_json(self) -> dict:
        try:
            return json.loads(self.data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"error": "Invalid JSON data"}

    def mark_sent(self):
        self.sent_time = time.time()
        print(f"📤 Сообщение {self} отправлено!")

    def mark_received(self):
        self.received_time = time.time()
        print(f"📥 Сообщение {self} получено!")

    def __repr__(self):
        sent = datetime.fromtimestamp(self.sent_time).isoformat() if self.sent_time else "None"
        received = datetime.fromtimestamp(self.received_time).isoformat() if self.received_time else "Not received"
        data_str = self.data.decode("utf-8", errors="ignore")
        return (
            f"Message(sender={self.sender_id}, receiver={self.receiver_id}, "
            f"algorithm={self.algorithm}, sent={sent}, received={received}, data='{data_str}')"
        )
