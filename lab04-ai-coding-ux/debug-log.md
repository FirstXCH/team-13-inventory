# บันทึกการ Debug ตามหลักฐาน 5 ขั้นตอน (Debug Log - Lab 4 ขั้นที่ 9-10)
**รายวิชา**: [31-407-102-302] วิศวกรรมซอฟต์แวร์ (Software Engineering) — Team 13  
**เป้าหมาย**: แก้ไขข้อผิดพลาดในโมดูล `discount.py` ตามชุดทดสอบทางการ `tests/test_discount.py` จนเขียวครบ 100%

---

## จุดที่ 1: คำนวณส่วนลดเปอร์เซ็นต์พื้นฐานผิดพลาด (`test_apply_discount_basic`)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_apply_discount_basic -v`
* **Assertion ที่ Fail**: `assert apply_discount(100.0, 10) == 90.0`
* **ผลลัพธ์ที่ได้จริง**: `assert 99.9 == 90.0`

### 2. Traceback
* **บรรทัดที่เกิด Error**: `tests/test_discount.py:8: AssertionError`
* โค้ดต้นทางอยู่ที่ `discount.py:5` ในฟังก์ชัน `apply_discount`

### 3. สมมติฐาน (Hypothesis)
> โค้ดต้นฉบับเขียนสมการทางคณิตศาสตร์ผิด โดยนำราคามาลบด้วยค่าเปอร์เซ็นต์หารด้วยร้อยตรง ๆ (`price - percent / 100`) แทนที่จะนำราคามาคูณกับสัดส่วนส่วนลด (`price * (percent / 100)`) ทำให้ยอดที่ลดกลายเป็นเพียงเศษสตางค์ (100 - 0.10 = 99.9)

### 4. การยืนยัน (Verification)
* ทดสอบคำนวณใน Python REPL:
  ```python
  >>> price = 100.0; percent = 10
  >>> price - percent / 100
  99.9
  >>> price * (1.0 - percent / 100.0)
  90.0
  ```
* ค่าที่คำนวณด้วยสูตรใหม่ได้ `90.0` ตรงตามเกณฑ์ของชุดทดสอบทุกประการ

### 5. Root cause และการแก้
* **Root cause**: เขียนสูตรคำนวณส่วนลดผิดหลักคณิตศาสตร์
* **การแก้ไข**: แก้สูตรใน `discount.py` เป็น `return round(price * (1.0 - percent / 100.0), 2)` พร้อมเพิ่ม Guard clause ป้องกันค่าติดลบ

---

## จุดที่ 2: รวมยอดซื้อหลายรายการแล้วลดส่วนลดผิดพลาด (`test_bulk_total`)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_bulk_total -v`
* **Assertion ที่ Fail**: `assert bulk_total([100.0, 100.0, 100.0], 10) == 270.0`
* **ผลลัพธ์ที่ได้จริง**: `assert 299.9 == 270.0`

### 2. Traceback
* **บรรทัดที่เกิด Error**: `tests/test_discount.py:18: AssertionError`
* เชื่อมโยงมาจาก `discount.py:12` ใน `bulk_total` ซึ่งเรียก `apply_discount(total, discount_percent)`

### 3. สมมติฐาน (Hypothesis)
> ฟังก์ชัน `bulk_total` รวมยอดเงินได้ถูกต้อง (`100 + 100 + 100 = 300`) แต่ส่งต่อยอดรวมไปให้ฟังก์ชัน `apply_discount` ซึ่งมี Bug ในการคำนวณเปอร์เซ็นต์ตามที่พบในจุดที่ 1

### 4. การยืนยัน (Verification)
* ทดสอบ Print ตรวจสอบค่าผลรวม:
  ```python
  total = sum([100.0, 100.0, 100.0])  # ได้ 300.0 ถูกต้อง
  ```
* เมื่อส่ง `300.0` เข้า `apply_discount` เดิม จะได้ `300 - 0.1 = 299.9` แต่เมื่อส่งเข้าฟังก์ชันที่แก้ไขแล้ว จะได้ `300 * 0.9 = 270.0`

### 5. Root cause และการแก้
* **Root cause**: อาการสืบเนื่อง (Cascading Failure) มาจากบั๊กในฟังก์ชัน `apply_discount` และสามารถปรับปรุงการรวมยอดให้ใช้ `sum(prices)` เพื่อความกระชับ
* **การแก้ไข**: ปรับปรุงฟังก์ชัน `apply_discount` และเขียน `bulk_total` ให้ใช้ `sum(prices)` ส่งต่อ

---

## จุดที่ 3: เกิด ZeroDivisionError เมื่อไม่มีรายการสินค้า (`test_average_price_empty`)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_average_price_empty -v`
* **Assertion ที่ Fail**: `assert average_price([]) == 0.0`
* **ผลลัพธ์ที่ได้จริง**: `ZeroDivisionError: division by zero`

### 2. Traceback
```text
tests/test_discount.py:28: in test_average_price_empty
    assert average_price([]) == 0.0
discount.py:18: in average_price
    return sum(prices) / len(prices)
E   ZeroDivisionError: division by zero
```

### 3. สมมติฐาน (Hypothesis)
> โค้ดไม่ได้ตรวจสอบค่าขอบเขตกรณีลิสต์ว่าง (`prices = []`) เมื่อเรียก `len(prices)` จะได้ผลลัพธ์เป็น 0 ส่งผลให้ตัวหารของสมการเป็นศูนย์จนเกิดข้อผิดพลาดทางคณิตศาสตร์

### 4. การยืนยัน (Verification)
* ทดสอบเรียก `len([])` ใน Python ได้ `0` การกระทำ `0 / 0` ทำให้ Python Raise `ZeroDivisionError` เสมอ
* การตรวจสอบ `if not prices:` จะดักจับกรณีลิสต์ว่างได้อย่างสมบูรณ์

### 5. Root cause และการแก้
* **Root cause**: ขาด Guard Clause ในการตรวจสอบ Input ลิสต์ว่างก่อนนำไปเป็นตัวหาร
* **การแก้ไข**: เพิ่มเงื่อนไข `if not prices: return 0.0` ก่อนทำการคำนวณค่าเฉลี่ย

---

## จุดที่ 4: คืนรายการสินค้าที่ถูกที่สุดผิดตำแหน่งและจำนวน (`test_cheapest_n`)

### 1. Reproduce
* **คำสั่งที่รัน**: `pytest tests/test_discount.py -k test_cheapest_n -v`
* **Assertion ที่ Fail**: `assert cheapest_n([50.0, 10.0, 30.0, 20.0], 2) == [10.0, 20.0]`
* **ผลลัพธ์ที่ได้จริง**: `assert [20.0] == [10.0, 20.0]`

### 2. Traceback
```text
tests/test_discount.py:33: in test_cheapest_n
    assert cheapest_n([50.0, 10.0, 30.0, 20.0], 2) == [10.0, 20.0]
E   AssertionError: assert [20.0] == [10.0, 20.0]
E     At index 0 diff: 20.0 != 10.0
E     Right contains one more item: 20.0
```

### 3. สมมติฐาน (Hypothesis)
> โค้ดใช้คำสั่ง Slice แบบผิดไวยากรณ์ `ordered[1:n]` โดยภาษา Python ทำงานแบบ Zero-indexed ทำให้ Index 1 เริ่มต้นที่สมาชิกตัวที่สอง (ตัดสินค้าที่ถูกที่สุดคือ 10.0 ทิ้งไป) และช่วง `[1:2]` ส่งคืนสมาชิกเพียงตัวเดียวคือ `[20.0]`

### 4. การยืนยัน (Verification)
* ทดสอบเรียงลำดับและ Slice:
  ```python
  >>> ordered = sorted([50.0, 10.0, 30.0, 20.0])
  >>> ordered
  [10.0, 20.0, 30.0, 50.0]
  >>> ordered[1:2]
  [20.0]
  >>> ordered[:2]
  [10.0, 20.0]
  ```
* ยืนยันว่าการใช้ `ordered[:n]` ได้ผลลัพธ์ถูกต้องทั้งลำดับและจำนวนชิ้น

### 5. Root cause และการแก้
* **Root cause**: ความเข้าใจผิดพลาดเกี่ยวกับ Index ของการ Slice ในภาษา Python (เริ่มต้นที่ 1 แทนที่จะเป็น 0)
* **การแก้ไข**: แก้ไขคำสั่ง Slice เป็น `return ordered[:n]` และเพิ่ม Guard clause `if n <= 0: return []`

---

## 3. สรุปกับดักที่ตั้งใจวางไว้ (Intentional Trap Analysis)
* ในชุดทดสอบ มีเคส **`test_apply_discount_zero`** ซึ่งทดสอบลดราคา 0% แล้ว Assert ได้ค่าเดิม (`250.0`)
* **ข้อพึงระวัง**: เคสนี้ผ่านสีเขียวตั้งแต่แรก แม้สูตรเดิมจะผิดก็ตาม เพราะ `250.0 - (0 / 100) = 250.0` แสดงให้เห็นชัดเจนว่า **"การที่ Test ผ่านบางข้อ ไม่ได้แปลว่าฟังก์ชันทำงานถูกต้องเสมอไป"** จึงต้องวิเคราะห์ Business Logic ร่วมด้วยเสมอ
