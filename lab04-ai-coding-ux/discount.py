"""
discount.py: โมดูลคำนวณส่วนลดและคูปอง (ฉบับแก้ไข Bug ครบทุกจุดตาม Lab 4 ขั้นที่ 10)
"""

def calculate_discount(total: float, tier: str = "STANDARD") -> float:
    """คำนวณส่วนลดตามขั้นบันไดยอดซื้อ"""
    if total < 0:
        raise ValueError("ยอดเงินรวมต้องไม่ติดลบ")

    if total == 0:
        return 0.0

    normalized_tier = tier.strip().upper()

    if normalized_tier == "TIER1":
        # เงื่อนไข: ยอดตั้งแต่ 1000 บาทขึ้นไป ลด 10%
        if total >= 1000.0:
            return round(total * 0.10, 2)
        return 0.0

    elif normalized_tier == "TIER2":
        # เงื่อนไข: ยอดตั้งแต่ 3000 บาทขึ้นไป ลด 15%
        if total >= 3000.0:
            return round(total * 0.15, 2)
        elif total >= 1000.0:
            return round(total * 0.10, 2)
        return 0.0

    return 0.0


def apply_coupon(total: float, coupon_code: str) -> float:
    """คำนวณยอดเงินสุทธิหลังหักคูปอง"""
    if total < 0:
        raise ValueError("ยอดเงินรวมต้องไม่ติดลบ")

    if not coupon_code:
        return total

    code = coupon_code.strip().upper()

    if code == "SAVE10":
        discount = 10.0
    elif code == "SUMMER50":
        discount = 50.0 if total >= 500.0 else 0.0
    else:
        discount = 0.0

    final_total = max(0.0, total - discount)
    return round(final_total, 2)
