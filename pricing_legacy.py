# pricing_legacy.py: โมดูลคิดราคาและส่วนลดฉบับเร่งรีบ (Legacy Code มี Code Smells ตามโจทย์ Lab 5 ขั้นที่ 6)

def calc(p, q, c_type="NORMAL", coupon="", is_wknd=False):
    # p: unit price, q: quantity, c_type: customer type
    if q <= 0 or p < 0:
        return 0.0

    tot = p * q
    d = 0.0

    # smell: magic numbers and nested conditions
    if c_type == "VIP":
        if tot > 1000:
            d = d + (tot * 0.15)
        else:
            d = d + (tot * 0.10)
    elif c_type == "MEMBER":
        if tot > 500:
            d = d + (tot * 0.05)
    else:
        d = 0.0

    if coupon == "SAVE10":
        d = d + 10.0
    elif coupon == "SUMMER50":
        if tot >= 500:
            d = d + 50.0

    if is_wknd:
        # weekend special discount 5% on subtotal
        d = d + (tot * 0.05)

    final = tot - d
    if final < 0:
        final = 0.0

    return round(final, 2)
