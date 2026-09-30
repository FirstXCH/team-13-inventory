# tests/test_pricing.py
# ทดสอบโมดูลที่จัดโค้ดใหม่ (src/pricing.py) เพื่อยืนยันว่าพฤติกรรมเดิมไม่เปลี่ยนและครอบคลุมทุก Branch 100%
from __future__ import annotations

import datetime

from src.pricing import LOG, PricingCalculator, PricingItem, calc, member_points


def test_refactored_calculator_basic():
    calc_service = PricingCalculator()
    subtotal = calc_service.calculate_items_subtotal([PricingItem("Notebook", 10, 20.0)])
    assert subtotal == 200.0
    final_price = calc_service.compute_tax_and_round(subtotal)
    assert final_price == 214.0


def test_refactored_item_quantity_tiers():
    calc_service = PricingCalculator()
    # <= 0 quantity
    zero_sub = calc_service.calculate_items_subtotal([PricingItem("Bad", 0, 10.0)])
    assert zero_sub == 0.0
    # Tier 100
    tier100 = calc_service.calculate_items_subtotal([PricingItem("BulkBk", 100, 10.0)])
    assert tier100 == 900.0
    # Tier 50
    tier50 = calc_service.calculate_items_subtotal([PricingItem("MidBk", 50, 10.0)])
    assert tier50 == 475.0


def test_refactored_member_discount():
    calc_service = PricingCalculator()
    # non-member
    tot, pts = calc_service.apply_member_discount(100.0, is_member=False)
    assert tot == 100.0 and pts == 0
    # member
    tot_m, pts_m = calc_service.apply_member_discount(200.0, is_member=True)
    assert tot_m == 190.0 and pts_m == 1


def test_refactored_coupon_discounts():
    calc_service = PricingCalculator()
    # None coupon
    assert calc_service.apply_coupon_discount(200.0, None) == 200.0
    # SAVE50
    assert calc_service.apply_coupon_discount(200.0, "SAVE50") == 150.0
    assert calc_service.apply_coupon_discount(40.0, "SAVE50") == 0.0
    # HALF
    assert calc_service.apply_coupon_discount(200.0, "HALF") == 100.0
    # NEWYEAR
    jan_date = datetime.date(2026, 1, 10)
    feb_date = datetime.date(2026, 2, 10)
    assert calc_service.apply_coupon_discount(200.0, "NEWYEAR", jan_date) == 160.0
    assert calc_service.apply_coupon_discount(200.0, "NEWYEAR", feb_date) == 200.0
    # Invalid coupon
    assert calc_service.apply_coupon_discount(200.0, "UNKNOWN") == 200.0


def test_refactored_calc_compatibility_with_characterization():
    jan_date = datetime.date(2026, 1, 10)
    items = [("ItemA", 50, 10.0)]
    assert calc(items) == 508.25
    assert calc(items, member="Tester") == 482.84
    assert member_points["Tester"] == 4
    assert calc(items, coupon="SAVE50") == 454.75
    assert calc(items, coupon="NEWYEAR", today=jan_date) == 406.6
    assert len(LOG) > 0
