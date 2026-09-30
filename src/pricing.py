# src/pricing.py
# โมดูลคำนวณราคาและส่วนลด (ฉบับ Refactor สะอาด ไร้ Code Smells ตาม Lab 5 ขั้นที่ 8)
from __future__ import annotations

import datetime
from collections.abc import Sequence
from dataclasses import dataclass

TAX_RATE: float = 0.07
VOLUME_TIER_HIGH_QTY: int = 100
VOLUME_TIER_HIGH_DISCOUNT: float = 0.10
VOLUME_TIER_MID_QTY: int = 50
VOLUME_TIER_MID_DISCOUNT: float = 0.05
MEMBER_DISCOUNT_RATE: float = 0.05
POINTS_PER_BAHT: int = 100
COUPON_NEWYEAR_DISCOUNT: float = 0.20


@dataclass(frozen=True)
class PricingItem:
    """แทนข้อมูลรายการสินค้าเพื่อหลีกเลี่ยง Magic Indices"""

    name: str
    quantity: int
    unit_price: float

    @classmethod
    def from_tuple(cls, item_tuple: tuple[str, int, float]) -> PricingItem:
        return cls(name=item_tuple[0], quantity=item_tuple[1], unit_price=item_tuple[2])

    def calculate_subtotal(self) -> float:
        if self.quantity <= 0:
            return 0.0
        base = self.quantity * self.unit_price
        if self.quantity >= VOLUME_TIER_HIGH_QTY:
            return base * (1.0 - VOLUME_TIER_HIGH_DISCOUNT)
        elif self.quantity >= VOLUME_TIER_MID_QTY:
            return base * (1.0 - VOLUME_TIER_MID_DISCOUNT)
        return base


class PricingCalculator:
    """คลาสคำนวณราคาสินค้าตามหลัก Single Responsibility และไม่มี Global State"""

    def __init__(self, tax_rate: float = TAX_RATE) -> None:
        self.tax_rate = tax_rate

    def calculate_items_subtotal(
        self,
        items: Sequence[tuple[str, int, float] | PricingItem],
    ) -> float:
        total = 0.0
        for raw in items:
            item = raw if isinstance(raw, PricingItem) else PricingItem.from_tuple(raw)
            total += item.calculate_subtotal()
        return total

    def apply_member_discount(self, total: float, is_member: bool) -> tuple[float, int]:
        if not is_member:
            return total, 0
        discounted = total * (1.0 - MEMBER_DISCOUNT_RATE)
        points_earned = int(discounted / POINTS_PER_BAHT)
        return discounted, points_earned

    def apply_coupon_discount(
        self,
        total: float,
        coupon: str | None,
        evaluation_date: datetime.date | None = None,
    ) -> float:
        if not coupon:
            return total
        normalized = coupon.strip().upper()
        if normalized == "SAVE50":
            return max(0.0, total - 50.0)
        elif normalized == "HALF":
            return total * 0.5
        elif normalized == "NEWYEAR":
            date = evaluation_date or datetime.date.today()
            if date.month == 1:
                return total * (1.0 - COUPON_NEWYEAR_DISCOUNT)
        return total

    def compute_tax_and_round(self, total: float) -> float:
        final_with_tax = total + (total * self.tax_rate)
        return round(final_with_tax, 2)


# Adapter Function เพื่อให้คง Interface เดิมของระบบ (Backward Compatibility 100%)
_default_calculator = PricingCalculator()
member_points: dict[str, int] = {}
LOG: list[tuple[str | None, float]] = []


def calc(
    items: list[tuple[str, int, float]],
    member: str | None = None,
    coupon: str | None = None,
    today: datetime.date | None = None,
) -> float:
    """ฟังก์ชัน Wrapper ที่คงรูปแบบคำสั่ง calc() เดิมทุกประการเพื่อให้ Test ผ่าน 100%"""
    subtotal = _default_calculator.calculate_items_subtotal(items)

    if member is not None:
        if member not in member_points:
            member_points[member] = 0
        subtotal, points = _default_calculator.apply_member_discount(subtotal, is_member=True)
        member_points[member] += points

    discounted = _default_calculator.apply_coupon_discount(subtotal, coupon, evaluation_date=today)
    final_price = _default_calculator.compute_tax_and_round(discounted)

    LOG.append((member, final_price))
    return final_price
