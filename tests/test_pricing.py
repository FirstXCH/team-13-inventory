from src.pricing import PriceCalculator, calc


def test_refactored_pricing_identical_to_legacy():
    # ตรวจสอบว่าฟังก์ชัน calc ใน src/pricing.py ให้ผลลัพธ์เหมือนเดิมทุกประการ
    assert calc(100.0, 2, c_type="NORMAL") == 200.0
    assert calc(100.0, 5, c_type="VIP") == 450.0
    assert calc(200.0, 10, c_type="VIP") == 1700.0
    assert calc(100.0, 4, c_type="MEMBER") == 400.0
    assert calc(100.0, 6, c_type="MEMBER") == 570.0
    assert calc(100.0, 1, coupon="SAVE10") == 90.0
    assert calc(100.0, 5, coupon="SUMMER50") == 450.0
    assert calc(100.0, 2, coupon="SUMMER50") == 200.0
    assert calc(100.0, 2, is_wknd=True) == 190.0
    assert calc(100.0, 0) == 0.0
    assert calc(-50.0, 2) == 0.0


def test_price_calculator_class_methods():
    # ทดสอบเมธอดของคลาส PriceCalculator โดยตรง
    assert PriceCalculator.calculate_membership_discount(1200.0, "VIP") == 180.0
    assert PriceCalculator.calculate_coupon_discount(600.0, "SUMMER50") == 50.0
    assert PriceCalculator.calculate_weekend_discount(200.0, True) == 10.0
