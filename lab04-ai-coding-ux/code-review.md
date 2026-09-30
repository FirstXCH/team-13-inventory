# รายงานการรีวิวโค้ดที่สร้างโดย AI (Code Review Report - Lab 4 ขั้นที่ 8)
**รายวิชา**: [31-407-102-302] วิศวกรรมซอฟต์แวร์ (Software Engineering) — Team 13  
**ไฟล์ที่ทำการรีวิว**: โค้ด Pull Request จาก AI (`inventory_service.py` แจกโดยผู้สอน)  
**มาตรฐานการรีวิว**: Human-in-the-Loop Code Review ตามคำถามนำ 4 ประเด็นหลัก

---

## 1. ผลการวิเคราะห์และ Review Comments รายเมธอด

### Comment 1: เมธอด `items_in_price_range()` — บรรทัดที่ 34-40
* **ชี้จุด (Location)**: เมธอด `items_in_price_range(self, low: float, high: float) -> list` บรรทัดที่ 38
* **ทำไมถึงผิด (Why it's wrong)**: ไม่ตรงกับ Docstring (Boundary Condition Mismatch) โดย Docstring กำหนดช่วงปิด `[low, high]` ซึ่งต้องนับรวมค่าขอบทั้งสองฝั่ง แต่โค้ดใช้เงื่อนไข `if low < item.price < high:` ซึ่งตัดสินค้าที่มีราคาเท่ากับ `low` หรือ `high` พอดีทิ้งไป
* **กรณีที่จะพัง (Breaking Example)**: มีสินค้า "สมุดบันทึก" ราคา 100.0 บาท เมื่อผู้ใช้เรียก `items_in_price_range(100.0, 200.0)` ฟังก์ชันจะคืนค่า `[]` (ไม่พบสินค้า) ทำให้ลูกค้ารายการสินค้าหายไปจากผลการค้นหา
* **เสนอทางแก้ (Proposed Fix)**:
  ```python
  if low <= item.price <= high:
      names.append(name)
  ```

---

### Comment 2: เมธอด `low_stock_report()` — บรรทัดที่ 43-49
* **ชี้จุด (Location)**: เมธอด `low_stock_report(self) -> list` บรรทัดที่ 47
* **ทำไมถึงผิด (Why it's wrong)**: ตรวจสอบเกณฑ์แจ้งเตือนสต็อกบกพร่องตามข้อกำหนด โดย Docstring ระบุชัดเจนว่า "ต่ำกว่าหรือเท่ากับเกณฑ์" แต่โค้ด AI เขียน `if item.quantity < self.LOW_STOCK_THRESHOLD:` ขาดเครื่องหมายเท่ากับ (`<=`)
* **กรณีที่จะพัง (Breaking Example)**: สินค้า "ปากกาเจล" มีสต็อกเหลือ 5 ด้ามพอดี (`quantity = 5`) และระบบมี `LOW_STOCK_THRESHOLD = 5` ฟังก์ชันนี้จะไม่ใส่ชื่อสินค้านี้ลงในรายงานเตือนภัย ทำให้ฝ่ายจัดซื้อไม่สั่งสินค้ามาเติมจนสินค้าหมดคลัง
* **เสนอทางแก้ (Proposed Fix)**:
  ```python
  if item.quantity <= self.LOW_STOCK_THRESHOLD:
      report.append(name)
  ```

---

### Comment 3: เมธอด `sell_batch()` — บรรทัดที่ 16-22
* **ชี้จุด (Location)**: เมธอด `sell_batch(self, orders: dict[str, int]) -> dict[str, int]` บรรทัดที่ 19-21
* **ทำไมถึงผิด (Why it's wrong)**: ขาดความเป็น Atomic Transaction (Partial State Mutation) โดยเมธอดทำการวนลูปตัดสต็อกทีละตัวผ่าน `self._inv.sell(name, amount)` หากสินค้าตัวหลังเกิดข้อผิดพลาด เช่น สต็อกไม่พอ (`ValueError`) หรือไม่พบสินค้า (`KeyError`) โค้ดจะหยุดทำงานทันที แต่สินค้าตัวแรก ๆ ที่ตัดสต็อกสำเร็จไปแล้วจะไม่ถูกย้อนคืน (Rollback) ทำให้ข้อมูลในคลังไม่ตรงกับความเป็นจริง
* **กรณีที่จะพัง (Breaking Example)**: ลูกค้าสั่งซื้อ `orders = {"BookA": 2, "BookB": 100}` โดย BookA มี 10 เล่ม (ตัดผ่าน เหลือ 8) แต่ BookB มีแค่ 1 เล่ม ฟังก์ชันจะ Raise `ValueError` การสั่งซื้อล้มเหลว แต่สต็อกของ BookA ถูกหักค้างไปแล้ว 2 เล่มฟรี ๆ
* **เสนอทางแก้ (Proposed Fix)**: ทำการตรวจสอบความพร้อมของสินค้าทุกรายการก่อน (Two-Phase / Dry Run) ก่อนเริ่มทำการตัดสต็อกจริง:
  ```python
  def sell_batch(self, orders: dict[str, int]) -> dict[str, int]:
      # Phase 1: ตรวจสอบความพร้อมของสินค้าทุกชิ้น
      for name, amount in orders.items():
          if name not in self._inv._items:
              raise KeyError(f"ไม่พบสินค้า '{name}'")
          if self._inv._items[name].quantity < amount:
              raise ValueError(f"สินค้า '{name}' มีไม่พอขาย")
      # Phase 2: ตัดสต็อกจริงเมื่อทุกรายการพร้อม
      result = {}
      for name, amount in orders.items():
          result[name] = self._inv.sell(name, amount)
      return result
  ```

---

### Comment 4: เมธอด `reserve()` — บรรทัดที่ 25-31
* **ชี้จุด (Location)**: เมธอด `reserve(self, name: str, amount: int) -> int` บรรทัดที่ 27-31
* **ทำไมถึงผิด (Why it's wrong)**: 
  1. ไม่ตรวจสอบว่า `amount <= 0` หรือไม่
  2. หากต้องการจองเกินจำนวนที่มี เงื่อนไข `if amount <= item.quantity - already:` จะเป็นเท็จและไม่ทำการบันทึกยอดจอง แต่ที่บรรทัด 31 ดึง `self._reserved[name]` ซึ่งหากสินค้านี้เพิ่งถูกเรียกจองครั้งแรก คีย์ `name` จะยังไม่เคยถูกสร้างใน `self._reserved` ส่งผลให้แครชด้วย `KeyError` ทันที
  3. ละเมิดหลักการ Encapsulation โดยเข้าถึง private attribute `_items` ของ Inventory โดยตรง
* **กรณีที่จะพัง (Breaking Example)**: สินค้าใหม่ "USB Drive" มีสต็อก 5 ชิ้น ผู้ใช้เรียก `reserve("USB Drive", 10)` ฟังก์ชันจะข้ามบรรทัดที่ 30 ไป แล้วรันบรรทัดที่ 31 `return item.quantity - self._reserved["USB Drive"]` เกิด `KeyError: 'USB Drive'` ทันที
* **เสนอทางแก้ (Proposed Fix)**:
  ```python
  def reserve(self, name: str, amount: int) -> int:
      if amount <= 0:
          raise ValueError("จำนวนที่ต้องการจองต้องมากกว่าศูนย์")
      if name not in self._inv._items:
          raise KeyError(f"ไม่พบสินค้า '{name}'")
      item = self._inv._items[name]
      already = self._reserved.get(name, 0)
      if amount > item.quantity - already:
          raise ValueError(f"สต็อกคงเหลือไม่พอสำหรับการจอง {amount} ชิ้น")
      self._reserved[name] = already + amount
      return item.quantity - self._reserved[name]
  ```

---

### Comment 5: เมธอด `concurrent_restock()` — บรรทัดที่ 52-57
* **ชี้จุด (Location)**: เมธอด `concurrent_restock(self, name: str, amount: int) -> int` บรรทัดที่ 54-56
* **ทำไมถึงผิด (Why it's wrong)**: Race Condition / Lost Update เนื่องจากโค้ดอ่านค่าสต็อกปัจจุบัน `current = self._inv._items[name].quantity` **ก่อนการเข้าสู่ Lock** (`with self._lock:`) ทำให้การล็อคไม่มีประโยชน์ หากมีสองเธรดอ่านค่าพร้อมกัน จะได้ค่า `current` เดียวกัน และเขียนทับผลลัพธ์กัน
* **กรณีที่จะพัง (Breaking Example)**: สินค้ามีสต็อก 10 ชิ้น เธรดที่ 1 เติม 5 ชิ้น และเธรดที่ 2 เติม 5 ชิ้น หากทั้งสองเธรดอ่าน `current = 10` ออกมาพร้อมกันก่อนเข้า Lock เธรดที่ 1 จะเขียน `10 + 5 = 15` และเธรดที่ 2 จะเขียน `10 + 5 = 15` ผลลัพธ์สต็อกกลายเป็น 15 ชิ้น แทนที่จะเป็น 20 ชิ้น (ยอดสต็อกหายไป 5 ชิ้น)
* **เสนอทางแก้ (Proposed Fix)**: ย้ายการอ่านและการปรับปรุงค่าให้อยู่ภายใน Lock อย่างสมบูรณ์:
  ```python
  def concurrent_restock(self, name: str, amount: int) -> int:
      with self._lock:
          return self._inv.restock(name, amount)
  ```

---

### Comment 6: เมธอด `average_unit_value()` — บรรทัดที่ 60-64
* **ชี้จุด (Location)**: เมธอด `average_unit_value(self) -> float` บรรทัดที่ 63-64
* **ทำไมถึงผิด (Why it's wrong)**: 
  1. เกิด `ZeroDivisionError` หากคลังสินค้าว่างเปล่า (`len(self._inv._items) == 0`)
  2. คำนวณผิดความหมายตาม Docstring โดย Docstring ระบุ "มูลค่าเฉลี่ยต่อชิ้นของสินค้าทั้งคลัง" แต่โค้ดนำไปหารด้วย `len(self._inv._items)` ซึ่งเป็นจำนวนประเภทสินค้า (SKU) ไม่ใช่จำนวนหน่วยชิ้นรวม (`total_quantity`)
* **กรณีที่จะพัง (Breaking Example)**: 
  - กรณีคลังว่าง: เรียกใช้ระบบตอนเริ่มต้น จะแครชด้วย `ZeroDivisionError: division by zero`
  - กรณีคำนวณผิด: มีสินค้าชนิดเดียวคือ "ปากกา" 100 ด้าม ด้ามละ 10 บาท (`total_value = 1,000` บาท) โค้ดจะนำ `1,000 / 1` ได้เฉลี่ยด้ามละ 1,000 บาท ทั้งที่ความจริงเฉลี่ยชิ้นละ 10 บาท
* **เสนอทางแก้ (Proposed Fix)**:
  ```python
  def average_unit_value(self) -> float:
      total_units = sum(item.quantity for item in self._inv._items.values())
      if total_units == 0:
          return 0.0
      return round(self._inv.get_total_value() / total_units, 2)
  ```

---

## 2. ตารางสรุปการจัดหมวดหมู่และระดับความรุนแรงของ Bug

| # | เมธอด | หมวดหมู่ (Category) | ระดับความรุนแรง (Severity) | สรุปปัญหา | กรณีที่ทำให้พัง |
|---|---|---|---|---|---|
| 1 | `items_in_price_range` | `correctness` | `medium` | ขาดเครื่องหมายเท่ากับในเงื่อนไขช่วงราคา | ค้นหาช่วง [100, 200] สินค้าราคา 100 ตกหล่น |
| 2 | `low_stock_report` | `correctness` | `high` | ขาดเครื่องหมายเท่ากับกับเกณฑ์สต็อกต่ำ | สต็อกเหลือ 5 ชิ้นเท่ากับเกณฑ์พอดี ไม่แจ้งเตือน |
| 3 | `sell_batch` | `correctness` | `high` | ไม่มี Rollback หากรายการหลังไม่สำเร็จ (Partial State) | สั่งซื้อ 2 รายการ ชิ้นแรกตัดสต็อกแต่ชิ้นสองพัง |
| 4 | `reserve` | `correctness` | `high` | จองเกินที่มีแล้วเกิด KeyError แครชระบบ | จองสินค้าใหม่เกินสต็อก ดึงคีย์ที่ยังไม่สร้าง |
| 5 | `concurrent_restock` | `concurrency` | `high` | อ่านค่านอก Lock ทำให้เกิด Race Condition | สองเธรดเติมของพร้อมกัน ข้อมูลอัปเดตสูญหาย |
| 6 | `average_unit_value` | `correctness` | `high` | ZeroDivisionError และหารจำนวน SKU แทนจำนวนชิ้น | คลังว่างเกิดแครชทันที หรือคิดมูลค่าต่อชิ้นเพี้ยน |

---
**สรุปความเห็นของ Reviewer**: PR ชุดนี้มีความเสี่ยงสูงมาก (**Block PR**) ห้าม Merge เข้าสู่ Branch Main จนกว่าจะได้รับการแก้ไขตามข้อเสนอแนะครบทั้ง 6 ข้อ
