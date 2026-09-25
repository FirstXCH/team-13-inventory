# ตารางจับคู่ Test Gap Analysis (Lab 5 ขั้นที่ 4)
**รายวิชา**: วิศวกรรมซอฟต์แวร์ — Team 13  
**การเปรียบเทียบชุดทดสอบที่ AI สร้างขึ้น กับกรณีทดสอบเสริมที่ทีมพัฒนาเพิ่มเติม**

| กรณีที่ AI ให้มา (Happy Path พื้นฐาน) | กรณีที่ขาดไป (Gap / Boundary / Edge Cases) | Test ที่เราเขียนเสริมใน `tests/test_inventory.py` |
|---|---|---|
| 1. สั่งซื้อสินค้าในสต็อกปกติแล้วยอดลดลง | สั่งซื้อสินค้าด้วยจำนวนเป็น 0 (Invalid Quantity) | `test_sell_zero_quantity_raises_value_error` |
| 2. สั่งซื้อสินค้าในสต็อกปกติแล้วยอดลดลง | สั่งซื้อสินค้าด้วยจำนวนติดลบ (Negative Quantity Attack) | `test_sell_negative_quantity_raises_value_error` |
| 3. สั่งซื้อสินค้าจนยอดเหลือน้อย | สั่งซื้อสินค้าเท่ากับสต็อกคงเหลือพอดีจนยอดเหลือ 0 ชิ้น | `test_sell_exact_stock_to_zero` |
| 4. สั่งซื้อสินค้าที่มีอยู่จริงในคลัง | สั่งซื้อสินค้ารหัสที่ไม่มีในระบบ (Non-existent Product ID) | `test_sell_nonexistent_product_raises_key_error` |
| 5. ซื้อสินค้าที่อยู่ในสถานะปกติ | ซื้อสินค้าที่ถูกปิดการขายชั่วคราว (`is_active=False`) | `test_sell_inactive_product_raises_value_error` |
| 6. ดึงรายการสินค้าสต็อกต่ำปกติ | ตรวจสอบกรณีคลังสินค้าว่างเปล่า (Empty Inventory) | `test_low_stock_items_empty_inventory` |
| 7. ดึงรายการสินค้าสต็อกต่ำปกติ | ตรวจสอบกรณี Threshold มีค่าติดลบ หรือค่า 0 พอดี | `test_low_stock_items_zero_threshold`<br>`test_low_stock_items_negative_threshold` |
