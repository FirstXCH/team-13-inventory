import pytest

from src.models import DigitalProduct, PhysicalProduct
from src.notifiers import EmailNotifier, SMSNotifier
from src.service import InventoryService

# ==============================================================================
# กลุ่มที่ 1: กฎข้อบังคับสินค้า 2 ชนิดสำหรับโครงงาน (Domain Business Rules)
# ==============================================================================

def test_physical_product_stock_deduction():
    """ทดสอบ: สินค้าที่จับต้องได้ต้องตัดสต็อกเมื่อทำการขายสำเร็จ"""
    service = InventoryService()
    book = PhysicalProduct(
        id="BOOK-P01",
        name="คู่มือ Database เล่มพิมพ์",
        price=350.0,
        category="หนังสือเรียน",
        stock=10,
        threshold=2,
    )
    service.add_product(book)

    result = service.sell_product("BOOK-P01", quantity=3)
    assert result["type"] == "Physical"
    assert result["remaining_stock"] == 7
    assert book.stock == 7


def test_physical_product_cannot_sell_beyond_stock():
    """ทดสอบ: สินค้าที่จับต้องได้ ห้ามขายเกินยอดคงเหลือ (โยน ValueError)"""
    service = InventoryService()
    book = PhysicalProduct(
        id="BOOK-P02",
        name="นวนิยายปกแข็ง",
        price=450.0,
        category="วรรณกรรม",
        stock=2,
        threshold=1,
    )
    service.add_product(book)

    with pytest.raises(ValueError, match="สินค้าคงเหลือไม่พอ"):
        service.sell_product("BOOK-P02", quantity=5)


def test_physical_product_deduct_direct_errors():
    """ทดสอบ: การเรียก deduct_stock โดยตรงด้วยค่าลบหรือเกินสต็อก"""
    book = PhysicalProduct(id="P0", name="Test", price=10.0, category="A", stock=5)
    with pytest.raises(ValueError, match="มากกว่า 0"):
        book.deduct_stock(0)
    with pytest.raises(ValueError, match="สินค้าคงเหลือไม่พอ"):
        book.deduct_stock(10)


def test_digital_product_no_stock_deduction():
    """ทดสอบ: สินค้าดิจิทัลไม่มียอดคงเหลือให้ตัด ขายกี่ครั้งสต็อกก็ไม่ลด"""
    service = InventoryService()
    ebook = DigitalProduct(
        id="EBOOK-D01",
        name="Building Calm Software (E-Book)",
        price=299.0,
        category="เทคโนโลยี",
        file_url="https://store.lampara.com/download/ebook-01.pdf",
    )
    service.add_product(ebook)

    res1 = service.sell_product("EBOOK-D01", quantity=1, order_status="Confirmed")
    assert res1["type"] == "Digital"
    assert res1["remaining_stock"] == "Unlimited (No Stock Deduction)"

    res2 = service.sell_product("EBOOK-D01", quantity=10, order_status="Confirmed")
    assert res2["type"] == "Digital"
    assert res2["remaining_stock"] == "Unlimited (No Stock Deduction)"


def test_digital_product_download_locked_when_pending():
    """ทดสอบ: สินค้าดิจิทัลเปิดลิงก์ดาวน์โหลดไม่ได้ก่อนคำสั่งซื้อจะยืนยัน (Pending)"""
    service = InventoryService()
    ebook = DigitalProduct(
        id="EBOOK-D02",
        name="The Quiet Algorithm (E-Book)",
        price=389.0,
        category="วิทยาการ",
        file_url="https://store.lampara.com/download/ebook-02.pdf",
    )
    service.add_product(ebook)

    result = service.sell_product("EBOOK-D02", quantity=1, order_status="Pending")
    assert result["download_unlocked"] is False
    assert result["download_url"] is None


def test_digital_product_download_unlocked_when_confirmed():
    """ทดสอบ: สินค้าดิจิทัลเปิดลิงก์ดาวน์โหลดได้เมื่อคำสั่งซื้อยืนยันแล้ว (Confirmed)"""
    service = InventoryService()
    ebook = DigitalProduct(
        id="EBOOK-D02",
        name="The Quiet Algorithm (E-Book)",
        price=389.0,
        category="วิทยาการ",
        file_url="https://store.lampara.com/download/ebook-02.pdf",
    )
    service.add_product(ebook)

    result = service.sell_product("EBOOK-D02", quantity=1, order_status="Confirmed")
    assert result["download_unlocked"] is True
    assert result["download_url"] == "https://store.lampara.com/download/ebook-02.pdf"


def test_low_stock_notification():
    """ทดสอบ: แจ้งเตือนเมื่อสินค้าจริงลดต่ำกว่า threshold (Observer Pattern)"""
    service = InventoryService()
    notifications = []

    class TestNotifier:
        def send(self, message: str) -> None:
            notifications.append(message)

    service.add_observer(TestNotifier())
    item = PhysicalProduct(
        id="ITEM-01",
        name="ปากกาเซ็นชื่อ",
        price=120.0,
        category="เครื่องเขียน",
        stock=6,
        threshold=5,
    )
    service.add_product(item)

    service.sell_product("ITEM-01", quantity=2)
    assert len(notifications) == 1
    assert "เตือน: สินค้า ปากกาเซ็นชื่อ คงเหลือ 4 ชิ้น" in notifications[0]


def test_notifiers_direct_send():
    """ทดสอบคลาส Notifier ตัวจริง (EmailNotifier & SMSNotifier)"""
    email_notifier = EmailNotifier("boss@store.com")
    email_notifier.send("ทดสอบ Email")
    sms_notifier = SMSNotifier("0899999999")
    sms_notifier.send("ทดสอบ SMS")


def test_get_stock_value():
    """ทดสอบการคำนวณมูลค่าสต็อกรวมในคลัง"""
    service = InventoryService()
    p1 = PhysicalProduct(id="P1", name="เล่ม 1", price=100.0, category="A", stock=5)
    p2 = PhysicalProduct(id="P2", name="เล่ม 2", price=200.0, category="A", stock=2)
    d1 = DigitalProduct(id="D1", name="Ebook", price=50.0, category="B")
    service.add_product(p1)
    service.add_product(p2)
    service.add_product(d1)
    # 100*5 + 200*2 = 900.0 (สินค้าดิจิทัลไม่นับมูลค่าสต็อก)
    assert service.get_stock_value() == 900.0


# ==============================================================================
# กลุ่มที่ 2: TDD 6 กรณีสำหรับ low_stock_items(threshold) (Lab 5 ขั้นที่ 2)
# ==============================================================================

def test_low_stock_items_all_above_threshold():
    """กรณี 1: ของทุกชิ้นมากกว่า threshold -> คืน list ว่าง"""
    service = InventoryService()
    p1 = PhysicalProduct(id="P1", name="สินค้า ก", price=100.0, category="A", stock=15)
    p2 = PhysicalProduct(id="P2", name="สินค้า ข", price=200.0, category="B", stock=20)
    service.add_product(p1)
    service.add_product(p2)
    assert service.low_stock_items(10) == []


def test_low_stock_items_exact_threshold():
    """กรณี 2: มีชิ้นที่เท่ากับ threshold พอดี -> ต้องถูกนับรวมด้วย"""
    service = InventoryService()
    p1 = PhysicalProduct(id="P1", name="สินค้า ก", price=100.0, category="A", stock=5)
    p2 = PhysicalProduct(id="P2", name="สินค้า ข", price=200.0, category="B", stock=8)
    service.add_product(p1)
    service.add_product(p2)
    assert service.low_stock_items(5) == ["สินค้า ก"]


def test_low_stock_items_multiple_sorted_by_name():
    """กรณี 3: มีหลายชิ้นเข้าเกณฑ์ -> ผลลัพธ์ต้องเรียงตามชื่อ ไม่ใช่ตามลำดับที่เพิ่ม"""
    service = InventoryService()
    p1 = PhysicalProduct(id="P1", name="สมุดบันทึก", price=50.0, category="A", stock=2)
    p2 = PhysicalProduct(id="P2", name="กรรไกร", price=40.0, category="B", stock=1)
    p3 = PhysicalProduct(id="P3", name="ดินสอ", price=10.0, category="C", stock=3)
    service.add_product(p1)
    service.add_product(p2)
    service.add_product(p3)
    # เรียงตามพยัญชนะไทย: กรรไกร -> ดินสอ -> สมุดบันทึก
    assert service.low_stock_items(5) == ["กรรไกร", "ดินสอ", "สมุดบันทึก"]


def test_low_stock_items_empty_inventory():
    """กรณี 4: คลังว่าง -> คืน list ว่าง ไม่ใช่ error"""
    service = InventoryService()
    assert service.low_stock_items(10) == []


def test_low_stock_items_zero_threshold():
    """กรณี 5: threshold เป็น 0 -> คืนเฉพาะชิ้นที่เหลือ 0 พอดี"""
    service = InventoryService()
    p1 = PhysicalProduct(id="P1", name="สินค้าหมด", price=100.0, category="A", stock=0)
    p2 = PhysicalProduct(id="P2", name="สินค้าเหลือหนึ่ง", price=100.0, category="A", stock=1)
    service.add_product(p1)
    service.add_product(p2)
    assert service.low_stock_items(0) == ["สินค้าหมด"]


def test_low_stock_items_negative_threshold():
    """กรณี 6: threshold ติดลบ -> คืน list ว่างอย่างปลอดภัย"""
    service = InventoryService()
    service.add_product(PhysicalProduct(id="P1", name="สินค้า ก", price=100.0, category="A", stock=5))
    assert service.low_stock_items(-1) == []


# ==============================================================================
# กลุ่มที่ 3: Edge Cases จับผิด AI (Lab 5 ขั้นที่ 4: Test Gap Analysis)
# ==============================================================================

def test_sell_zero_quantity_raises_value_error():
    """Edge Case: สั่งซื้อจำนวน 0 ชิ้น ต้องโยน ValueError ทันที"""
    service = InventoryService()
    service.add_product(PhysicalProduct(id="P1", name="หนังสือ", price=100.0, category="A", stock=10))
    with pytest.raises(ValueError, match="มากกว่า 0"):
        service.sell_product("P1", quantity=0)


def test_sell_negative_quantity_raises_value_error():
    """Edge Case: สั่งซื้อจำนวนติดลบ ต้องโยน ValueError ทันที"""
    service = InventoryService()
    service.add_product(PhysicalProduct(id="P1", name="หนังสือ", price=100.0, category="A", stock=10))
    with pytest.raises(ValueError, match="มากกว่า 0"):
        service.sell_product("P1", quantity=-5)


def test_sell_exact_stock_to_zero():
    """Edge Case: ขายสินค้าหมดเกลี้ยงพอดี (สต็อกเหลือ 0) ต้องสำเร็จและแจ้งเตือนถูกต้อง"""
    service = InventoryService()
    p = PhysicalProduct(id="P1", name="หนังสือ", price=100.0, category="A", stock=5, threshold=1)
    service.add_product(p)
    res = service.sell_product("P1", quantity=5)
    assert res["remaining_stock"] == 0


def test_sell_nonexistent_product_raises_key_error():
    """Edge Case: ขายสินค้ารหัสที่ไม่มีอยู่ในคลัง ต้องโยน KeyError"""
    service = InventoryService()
    with pytest.raises(KeyError, match="ไม่พบสินค้ารหัส"):
        service.sell_product("UNKNOWN_ID", quantity=1)


def test_sell_inactive_product_raises_value_error():
    """Edge Case: สินค้าที่ปิดการขาย (is_active=False) ต้องไม่สามารถสั่งซื้อได้"""
    service = InventoryService()
    item = PhysicalProduct(
        id="P1", name="สินค้าเลิกผลิต", price=100.0, category="A", stock=10, is_active=False
    )
    service.add_product(item)
    with pytest.raises(ValueError, match="ถูกปิดการขายแล้ว"):
        service.sell_product("P1", quantity=1)
