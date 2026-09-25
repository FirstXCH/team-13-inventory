"""
pricing.py: โมดูลคำนวณราคาและส่วนลดที่ผ่านการ Refactoring ตามหลัก Clean Code & SOLID
(Lab 5 ขั้นที่ 8: พฤติกรรมทุกอย่างคงเดิม 100% ตรงตาม Characterization Test)
"""

from dataclasses import dataclass
from typing import Final

# ค่าคงที่อัตราส่วนลด (แก้ Magic Numbers)
VIP_HIGH_THRESHOLD: Final[float] = 1000.0
VIP_HIGH_DISCOUNT_RATE: Final[float] = 0.15
VIP_BASE_DISCOUNT_RATE: Final[float] = 0.10

MEMBER_THRESHOLD: Final[float] = 500.0
MEMBER_DISCOUNT_RATE: Final[float] = 0.05

WEEKEND_DISCOUNT_RATE: Final[float] = 0.05
SUMMER_COUPON_MIN_TOTAL: Final[float] = 500.0
SUMMER_COUPON_DISCOUNT: Final[float] = 50.0
SAVE10_COUPON_DISCOUNT: Final[float] = 10.0


@dataclass(frozen=True)
class PricingRequest:
    unit_price: float
    quantity: int
    customer_type: str = "NORMAL"
    coupon_code: str = ""
    is_weekend: bool = False


class PriceCalculator:
    """คลาสคำนวณราคาและส่วนลดตามหลัก SRP"""

    @staticmethod
    def calculate_membership_discount(total: float, customer_type: str) -> float:
        c_type = customer_type.upper()
        if c_type == "VIP":
            rate = VIP_HIGH_DISCOUNT_RATE if total > VIP_HIGH_THRESHOLD else VIP_BASE_DISCOUNT_RATE
            return total * rate
        if c_type == "MEMBER" and total > MEMBER_THRESHOLD:
            return total * MEMBER_DISCOUNT_RATE
        return 0.0

    @staticmethod
    def calculate_coupon_discount(total: float, coupon_code: str) -> float:
        code = coupon_code.strip().upper()
        if code == "SAVE10":
            return SAVE10_COUPON_DISCOUNT
        if code == "SUMMER50" and total >= SUMMER_COUPON_MIN_TOTAL:
            return SUMMER_COUPON_DISCOUNT
        return 0.0

    @staticmethod
    def calculate_weekend_discount(total: float, is_weekend: bool) -> float:
        return total * WEEKEND_DISCOUNT_RATE if is_weekend else 0.0

    @classmethod
    def calculate_final_price(
        cls,
        price: float,
        qty: int,
        customer_type: str = "NORMAL",
        coupon_code: str = "",
        is_weekend: bool = False,
    ) -> float:
        if qty <= 0 or price < 0:
            return 0.0

        subtotal = price * qty
        discount = (
            cls.calculate_membership_discount(subtotal, customer_type)
            + cls.calculate_coupon_discount(subtotal, coupon_code)
            + cls.calculate_weekend_discount(subtotal, is_weekend)
        )

        final_price = max(0.0, subtotal - discount)
        return round(final_price, 2)


# ฟังก์ชัน Wrapper เพื่อให้ทำงานร่วมกับ Characterization Test ชุดเดิมได้ 100%
def calc(
    p: float, q: int, c_type: str = "NORMAL", coupon: str = "", is_wknd: bool = False
) -> float:
    return PriceCalculator.calculate_final_price(
        price=p,
        qty=q,
        customer_type=c_type,
        coupon_code=coupon,
        is_weekend=is_wknd,
    )
