from src.models import DigitalProduct, PhysicalProduct
from src.notifiers import Notifier


class InventoryService:
    """ระบบจัดการคลังสินค้าและแคตตาล็อก"""

    def __init__(self):
        self.products: dict[str, PhysicalProduct | DigitalProduct] = {}
        self._observers: list[Notifier] = []

    def add_observer(self, observer: Notifier) -> None:
        """ลงทะเบียนผู้รับการแจ้งเตือน"""
        self._observers.append(observer)

    def _notify(self, message: str) -> None:
        """ส่งการแจ้งเตือนไปยังผู้รับทั้งหมด (Observer Pattern)"""
        for observer in self._observers:
            observer.send(message)

    def add_product(self, product: PhysicalProduct | DigitalProduct) -> None:
        """เพิ่มสินค้าเข้าสู่ระบบ"""
        self.products[product.id] = product

    def sell_product(
        self, product_id: str, quantity: int, order_status: str = "Pending"
    ) -> dict:
        """
        ประมวลผลการขายตามชนิดสินค้า (กฎข้อบังคับ 11 ก.ย.):
        1. สินค้าที่จับต้องได้ (Physical): ต้องตัดสต็อก และห้ามขายเกินยอดคงเหลือ
        2. สินค้าดิจิทัล (Digital): ไม่มีการตัดสต็อก ขายได้ไม่จำกัด แต่ตรวจสอบสิทธิ์ดาวน์โหลด
        """
        if quantity <= 0:
            raise ValueError("จำนวนสินค้าที่ขายต้องมากกว่า 0")

        if product_id not in self.products:
            raise KeyError(f"ไม่พบสินค้ารหัส {product_id} ในระบบ")

        product = self.products[product_id]

        if not product.is_active:
            raise ValueError(f"สินค้า {product.name} ถูกปิดการขายแล้ว")

        if isinstance(product, PhysicalProduct):
            product.deduct_stock(quantity)
            if product.is_low_stock():
                msg = (
                    f"เตือน: สินค้า {product.name} คงเหลือ {product.stock} ชิ้น "
                    f"(ต่ำกว่าเกณฑ์ {product.threshold})"
                )
                self._notify(msg)
            return {
                "product_id": product.id,
                "type": "Physical",
                "sold_quantity": quantity,
                "remaining_stock": product.stock,
                "download_link": None,
            }

        elif isinstance(product, DigitalProduct):
            is_unlocked = product.can_access_download(order_status)
            download_url = product.file_url if is_unlocked else None
            return {
                "product_id": product.id,
                "type": "Digital",
                "sold_quantity": quantity,
                "remaining_stock": "Unlimited (No Stock Deduction)",
                "download_unlocked": is_unlocked,
                "download_url": download_url,
            }

    def low_stock_items(self, threshold: int) -> list[str]:
        """
        โจทย์ Lab 5 (TDD ขั้นที่ 2-3):
        คืนรายชื่อสินค้าที่มีของเหลือน้อยกว่าหรือเท่ากับ threshold โดยเรียงตามชื่อ
        """
        if threshold < 0:
            return []
        matching_names = [
            p.name
            for p in self.products.values()
            if isinstance(p, PhysicalProduct) and p.stock <= threshold
        ]
        return sorted(matching_names)

    def get_stock_value(self) -> float:
        """คำนวณมูลค่ารวมของสินค้าที่มีสต็อกในคลัง"""
        total = 0.0
        for p in self.products.values():
            if isinstance(p, PhysicalProduct):
                total += p.price * p.stock
        return total


# Alias สำหรับความเข้ากันได้กับโจทย์ Lab 5
Inventory = InventoryService
