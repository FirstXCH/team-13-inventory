from typing import Protocol

class Notifier(Protocol):
    """Protocol (Interface) สำหรับการแจ้งเตือน"""
    def send(self, message: str) -> None:
        ...

class EmailNotifier:
    """แจ้งเตือนผ่านอีเมล"""
    def send(self, message: str) -> None:
        print(f"[Email] {message}")

class SMSNotifier:
    """แจ้งเตือนผ่าน SMS"""
    def send(self, message: str) -> None:
        print(f"[SMS] {message}")

class NotifierFactory:
    """Factory สำหรับสร้าง Notifier ตามช่องทางที่ระบุ (แก้การละเมิด OCP)"""
    @staticmethod
    def create(channel: str) -> Notifier:
        if channel.lower() == "email":
            return EmailNotifier()
        elif channel.lower() == "sms":
            return SMSNotifier()
        else:
            raise ValueError(f"ไม่รองรับช่องทางการแจ้งเตือน: {channel}")