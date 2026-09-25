import pytest
from discount import apply_coupon, calculate_discount


def test_tiered_discount_boundary():
    # ทดสอบค่าขอบเขต 1000 บาท ต้องได้รับส่วนลด 10% (= 100.0)
    assert calculate_discount(1000.0, "TIER1") == 100.0
    # ต่ำกว่า 1000 บาท ต้องไม่ได้ส่วนลด
    assert calculate_discount(999.99, "TIER1") == 0.0
    # ยอด 3000 บาท TIER2 ต้องได้ 15% (= 450.0)
    assert calculate_discount(3000.0, "TIER2") == 450.0


def test_negative_total_raises_error():
    with pytest.raises(ValueError, match="ยอดเงินรวมต้องไม่ติดลบ"):
        calculate_discount(-50.0, "TIER1")

    with pytest.raises(ValueError, match="ยอดเงินรวมต้องไม่ติดลบ"):
        apply_coupon(-100.0, "SAVE10")


def test_coupon_case_insensitive():
    # ทดสอบว่ารหัสคูปองพิมพ์ตัวเล็กต้องใช้ได้ผลเท่ากับตัวใหญ่
    assert apply_coupon(100.0, "save10") == 90.0
    assert apply_coupon(100.0, "SAVE10") == 90.0
    assert apply_coupon(600.0, "summer50") == 550.0
    assert apply_coupon(200.0, "summer50") == 200.0


def test_zero_total():
    assert calculate_discount(0.0, "TIER1") == 0.0
    assert apply_coupon(0.0, "SAVE10") == 0.0
