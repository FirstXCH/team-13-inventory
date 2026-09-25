from dataclasses import dataclass


@dataclass
class Product:
    """คลาสพื้นฐานสำหรับสินค้าในระบบ"""
    id: str
    name: str
    price: float
    category: str
    is_active: bool = True

@dataclass
class PhysicalProduct(Product):
    """สินค้าที่จับต้องได้ (เช่น หนังสือเล่มกระดาษ, อุปกรณ์) - มีสต็อกและต้องตัดยอดคงเหลือ"""
    stock: int = 0
    threshold: int = 5

    def deduct_stock(self, quantity: int) -> bool:
        """ตัดยอดคงเหลือสินค้า โดยไม่อนุญาตให้สั่งซื้อเกินจำนวนที่มี"""
        if quantity <= 0:
            raise ValueError("จำนวนที่สั่งซื้อต้องมากกว่า 0")
        if quantity > self.stock:
            raise ValueError(f"สินค้าคงเหลือไม่พอ (มี {self.stock} ชิ้น แต่ต้องการ {quantity} ชิ้น)")
        self.stock -= quantity
        return True

    def is_low_stock(self) -> bool:
        """ตรวจสอบว่าสินค้าต่ำกว่าเกณฑ์เตือนหรือไม่"""
        return self.stock <= self.threshold

@dataclass
class DigitalProduct(Product):
    """สินค้าดิจิทัล (เช่น E-Book ไฟล์ PDF/EPUB) - ไม่มียอดคงเหลือให้ตัด ขายได้ไม่จำกัด"""
    file_url: str = ""
    file_format: str = "PDF"

    def can_access_download(self, order_status: str) -> bool:
        """กฎความปลอดภัย: เปิดสิทธิ์ดาวน์โหลดได้เฉพาะเมื่อคำสั่งซื้อได้รับการยืนยัน (Confirmed) แล้วเท่านั้น"""
        valid_statuses = ["Confirmed", "Completed", "Paid"]
        return order_status in valid_statuses

@dataclass
class StockTransaction:
    """ประวัติการทำรายการสต็อก"""
    product_id: str
    amount: int
    is_inbound: bool
