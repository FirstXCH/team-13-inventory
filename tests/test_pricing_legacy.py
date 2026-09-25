from pricing_legacy import calc


def test_legacy_pricing_normal_customer_no_discount():
    assert calc(100.0, 2, c_type="NORMAL") == 200.0


def test_legacy_pricing_vip_under_1000():
    # 100 * 5 = 500 -> VIP 10% = 50 -> 450.0
    assert calc(100.0, 5, c_type="VIP") == 450.0


def test_legacy_pricing_vip_over_1000():
    # 200 * 10 = 2000 -> VIP 15% = 300 -> 1700.0
    assert calc(200.0, 10, c_type="VIP") == 1700.0


def test_legacy_pricing_member_under_500():
    # 100 * 4 = 400 -> No discount
    assert calc(100.0, 4, c_type="MEMBER") == 400.0


def test_legacy_pricing_member_over_500():
    # 100 * 6 = 600 -> Member 5% = 30 -> 570.0
    assert calc(100.0, 6, c_type="MEMBER") == 570.0


def test_legacy_pricing_coupons():
    # SAVE10 coupon
    assert calc(100.0, 1, coupon="SAVE10") == 90.0
    # SUMMER50 coupon when total >= 500
    assert calc(100.0, 5, coupon="SUMMER50") == 450.0
    # SUMMER50 coupon when total < 500 (no coupon applied)
    assert calc(100.0, 2, coupon="SUMMER50") == 200.0


def test_legacy_pricing_weekend_discount():
    # 100 * 2 = 200 -> weekend 5% = 10 -> 190.0
    assert calc(100.0, 2, is_wknd=True) == 190.0


def test_legacy_pricing_invalid_inputs():
    assert calc(100.0, 0) == 0.0
    assert calc(-50.0, 2) == 0.0
