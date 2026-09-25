# บันทึกการ Debug ตามหลักฐาน 5 ขั้นตอน (Debug Log - Lab 4 ขั้นที่ 9-10)
**รายวิชา**: วิศวกรรมซอฟต์แวร์ — Team 13  
**เป้าหมาย**: แก้ไขข้อผิดพลาดในโมดูลคำนวณส่วนลด `discount.py` จนชุดทดสอบ `tests/test_discount.py` ผ่าน 100%

---

## จุดที่ 1: ข้อผิดพลาดการคำนวณส่วนลดตามขั้นบันได (Tiered Discount Bug)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_tiered_discount_boundary`
* **Assertion ที่ Fail**: `assert calculate_discount(1000.0, "TIER1") == 100.0` แต่ได้ผลลัพธ์เป็น `0.0`

### 2. Traceback
* **บรรทัดที่ Error เกิด**: `discount.py:14` ในฟังก์ชัน `calculate_discount`
* Traceback ชี้ว่าโค้ดตรวจสอบเงื่อนไข `if total > 1000:` จึงข้ามเงื่อนไขลด 10% เมื่อยอดซื้อเท่ากับ 1,000 บาทพอดี

### 3. สมมติฐาน (Hypothesis)
> โค้ดเดิมเขียนตัวดำเนินการเปรียบเทียบผิดพลาด โดยใช้เครื่องหมาย "มากกว่า" (`>`) แทนที่จะเป็น "มากกว่าหรือเท่ากับ" (`>=`) ตามข้อกำหนดของส่วนลดขั้นบันได

### 4. การยืนยัน (Verification)
* พิมพ์ค่าตรวจสอบ: `print(f"DEBUG: total={total}, condition_met={total >= 1000}")`
* พบว่าเมื่อส่ง `total = 1000.0` ค่า `total > 1000` คืนค่า `False` แต่ `total >= 1000` คืนค่า `True`

### 5. Root Cause และการแก้ไข
* **Root Cause จริง**: การกำหนด Boundary Condition ผิดพลาดในคำสั่งเงื่อนไข
* **การแก้ไข**: แก้ไขบรรทัดที่ 14 ใน `discount.py` จาก `if total > 1000:` เป็น `if total >= 1000:`

---

## จุดที่ 2: ข้อผิดพลาดเมื่อป้อนยอดเงินติดลบหรือเป็นศูนย์ (Negative/Zero Boundary Bug)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_negative_total_raises_error`
* **Assertion ที่ Fail**: `with pytest.raises(ValueError)` แต่ฟังก์ชันคืนค่า `-50.0` ออกมาโดยไม่โยนข้อผิดพลาด

### 2. Traceback
* **บรรทัดที่ Error เกิด**: `discount.py:8` ฟังก์ชันไม่ได้ตรวจสอบค่าของพารามิเตอร์ขาเข้าก่อนนำไปคำนวณ

### 3. สมมติฐาน (Hypothesis)
> ฟังก์ชันขาด Guard Clause ในการตรวจสอบ Input Validation สำหรับตัวเลขยอดเงินที่ต้องไม่ติดลบ

### 4. การยืนยัน (Verification)
* ทดลองส่ง `calculate_discount(-100.0, "TIER1")` แล้วได้ส่วนลดติดลบ ซึ่งขัดต่อหลักการทางธุรกิจ

### 5. Root Cause และการแก้ไข
* **Root Cause จริง**: ขาดการตรวจสอบความถูกต้องของข้อมูลนำเข้า (Missing Input Sanitization)
* **การแก้ไข**: เพิ่มโค้ดตรวจสอบที่ต้นฟังก์ชัน:
  ```python
  if total < 0:
      raise ValueError("ยอดเงินรวมต้องไม่ติดลบ")
  ```

---

## จุดที่ 3: ข้อผิดพลาดเรื่องตัวพิมพ์เล็ก-ใหญ่ของรหัสคูปอง (Case Sensitivity Bug)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_coupon_case_insensitive`
* **Assertion ที่ Fail**: `assert apply_coupon(100.0, "save10") == 90.0` แต่ได้ `100.0`

### 2. Traceback
* **บรรทัดที่ Error เกิด**: `discount.py:28` โค้ดเปรียบเทียบ `if coupon == "SAVE10":` ตรงๆ

### 3. สมมติฐาน (Hypothesis)
> โค้ดไม่ได้ทำการ Normalize ข้อความสตริงก่อนเปรียบเทียบ ทำให้ผู้ใช้ที่พิมพ์ตัวพิมพ์เล็กไม่ได้รับส่วนลด

### 4. การยืนยัน (Verification)
* ตรวจสอบ `"save10" == "SAVE10"` ได้ผลเป็น `False`

### 5. Root Cause และการแก้ไข
* **Root Cause จริง**: ไม่ได้จัดการเรื่อง String Normalization
* **การแก้ไข**: แปลงรหัสคูปองเป็นตัวพิมพ์ใหญ่ก่อนตรวจสอบ: `if coupon.strip().upper() == "SAVE10":`
