# tests/test_pricing_legacy.py
# Characterization Tests: ตรึงพฤติกรรมเดิมของ pricing_legacy.py ให้ครบถ้วน 100%
import datetime

import pytest

import pricing_legacy
from pricing_legacy import calc


@pytest.fixture(autouse=True)
def reset_global_state():
    """ล้าง Global State ของ pricing_legacy ก่อนและหลังแต่ละ Test ป้องกัน Test Interference"""
    pricing_legacy.member_points.clear()
    pricing_legacy.LOG.clear()
    yield
    pricing_legacy.member_points.clear()
    pricing_legacy.LOG.clear()


def test_basic_pricing_without_discount():
    # สินค้า 10 ชิ้น ชิ้นละ 20.0 = 200 + VAT 7% = 214.0
    items = [("Pen", 10, 20.0)]
    assert calc(items) == 214.0


def test_volume_discount_50_tier():
    # ซื้อ 50 ชิ้น ได้ลด 5% -> 50 * 10 * 0.95 = 475.0 + VAT 7% = 508.25
    items = [("Book", 50, 10.0)]
    assert calc(items) == 508.25


def test_volume_discount_100_tier():
    # ซื้อ 100 ชิ้น ได้ลด 10% -> 100 * 10 * 0.90 = 900.0 + VAT 7% = 963.0
    items = [("Book", 100, 10.0)]
    assert calc(items) == 963.0


def test_member_discount_and_points_accumulation():
    # สมาชิกได้ลด 5% และสะสมแต้ม 1 แต้มต่อ 100 บาท
    # 200 * 0.95 = 190.0 -> VAT 7% = 203.3, แต้ม = 1
    items = [("Pen", 10, 20.0)]
    assert calc(items, member="Somchai") == 203.3
    assert pricing_legacy.member_points["Somchai"] == 1


def test_coupon_save50():
    # คูปองลด 50 บาทตรงๆ -> (200 - 50) = 150 + VAT 7% = 160.5
    items = [("Pen", 10, 20.0)]
    assert calc(items, coupon="SAVE50") == 160.5


def test_coupon_half():
    # คูปองลด 50% -> (200 * 0.5) = 100 + VAT 7% = 107.0
    items = [("Pen", 10, 20.0)]
    assert calc(items, coupon="HALF") == 107.0


def test_coupon_newyear_in_january():
    # คูปองปีใหม่ลด 20% เฉพาะเดือนมกราคม -> 200 * 0.8 = 160 + VAT 7% = 171.2
    items = [("Pen", 10, 20.0)]
    jan_date = datetime.date(2026, 1, 15)
    assert calc(items, coupon="NEWYEAR", today=jan_date) == 171.2


def test_coupon_newyear_outside_january():
    # คูปองปีใหม่ใช้เดือนอื่นไม่ได้ลด -> 200 + VAT 7% = 214.0
    items = [("Pen", 10, 20.0)]
    feb_date = datetime.date(2026, 2, 15)
    assert calc(items, coupon="NEWYEAR", today=feb_date) == 214.0


def test_zero_or_negative_quantity_ignored():
    # สินค้าที่มีจำนวน <= 0 ต้องถูกข้าม
    items = [("BadItem", 0, 50.0), ("Negative", -5, 100.0)]
    assert calc(items) == 0.0


def test_logging_side_effect():
    # ตรวจสอบการบันทึก LOG
    items = [("Pen", 10, 20.0)]
    calc(items, member="Alice")
    assert len(pricing_legacy.LOG) == 1
    assert pricing_legacy.LOG[0] == ("Alice", 203.3)
