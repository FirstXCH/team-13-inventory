from typing import Protocol


class Notifier(Protocol):
    """Interface กลางสำหรับผู้ส่งการแจ้งเตือน (DIP & OCP)"""
    def send(self, message: str) -> None:
        ...

class EmailNotifier:
    """ผู้ส่งการแจ้งเตือนทาง Email"""
    def __init__(self, target_email: str = "manager@store.com"):
        self.target_email = target_email

    def send(self, message: str) -> None:
        print(f"[Email to {self.target_email}] {message}")

class SMSNotifier:
    """ผู้ส่งการแจ้งเตือนทาง SMS"""
    def __init__(self, phone_number: str = "0812345678"):
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        print(f"[SMS to {self.phone_number}] {message}")
