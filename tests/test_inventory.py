# -*- coding: utf-8 -*-
import pytest
from src.models import PhysicalProduct, DigitalProduct
from src.service import InventoryService

def test_physical_product_stock_deduction():
    """ทดสอบ: สินค้าที่จับต้องได้ต้องตัดสต็อกเมื่อทำการขาย"""
    service = InventoryService()
    book = PhysicalProduct(id="BOOK-P01", name="คู่มือ Database เล่มพิมพ์", price=350.0, category="หนังสือเรียน", stock=10, threshold=2)
    service.add_product(book)

    result = service.sell_product("BOOK-P01", quantity=3)
    assert result["type"] == "Physical"
    assert result["remaining_stock"] == 7
    assert book.stock == 7

def test_physical_product_cannot_sell_beyond_stock():
    """ทดสอบ: สินค้าที่จับต้องได้ ห้ามขายเกินยอดคงเหลือ (โยน ValueError)"""
    service = InventoryService()
    book = PhysicalProduct(id="BOOK-P02", name="นวนิยายปกแข็ง", price=450.0, category="วรรณกรรม", stock=2, threshold=1)
    service.add_product(book)

    with pytest.raises(ValueError, match="สินค้าคงเหลือไม่พอ"):
        service.sell_product("BOOK-P02", quantity=5)

def test_digital_product_no_stock_deduction():
    """ทดสอบ: สินค้าดิจิทัลไม่มียอดคงเหลือให้ตัด ขายกี่ครั้งสต็อกก็ไม่ลด"""
    service = InventoryService()
    ebook = DigitalProduct(id="EBOOK-D01", name="Building Calm Software (E-Book)", price=299.0, category="เทคโนโลยี", file_url="https://store.lampara.com/download/ebook-01.pdf")
    service.add_product(ebook)

    res1 = service.sell_product("EBOOK-D01", quantity=1, order_status="Confirmed")
    assert res1["type"] == "Digital"
    assert res1["remaining_stock"] == "Unlimited (No Stock Deduction)"

    res2 = service.sell_product("EBOOK-D01", quantity=10, order_status="Confirmed")
    assert res2["type"] == "Digital"
    assert res2["remaining_stock"] == "Unlimited (No Stock Deduction)"

def test_digital_product_download_locked_when_pending():
    """ทดสอบ: สินค้าดิจิทัลเปิดลิงก์ดาวน์โหลดไม่ได้ก่อนคำสั่งซื้อจะยืนยัน (สถานะ Pending)"""
    service = InventoryService()
    ebook = DigitalProduct(id="EBOOK-D02", name="The Quiet Algorithm (E-Book)", price=389.0, category="วิทยาการ", file_url="https://store.lampara.com/download/ebook-02.pdf")
    service.add_product(ebook)

    result = service.sell_product("EBOOK-D02", quantity=1, order_status="Pending")
    assert result["download_unlocked"] is False
    assert result["download_url"] is None

def test_digital_product_download_unlocked_when_confirmed():
    """ทดสอบ: สินค้าดิจิทัลเปิดลิงก์ดาวน์โหลดได้เมื่อคำสั่งซื้อยืนยันแล้ว (สถานะ Confirmed)"""
    service = InventoryService()
    ebook = DigitalProduct(id="EBOOK-D02", name="The Quiet Algorithm (E-Book)", price=389.0, category="วิทยาการ", file_url="https://store.lampara.com/download/ebook-02.pdf")
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
    book = PhysicalProduct(id="BOOK-P03", name="ปากกาเซ็นชื่อ", price=120.0, category="เครื่องเขียน", stock=6, threshold=5)
    service.add_product(book)

    service.sell_product("BOOK-P03", quantity=2)
    assert len(notifications) == 1
    assert "เตือน: สินค้า ปากกาเซ็นชื่อ คงเหลือ 4 ชิ้น" in notifications[0]
