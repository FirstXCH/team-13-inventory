# รายการ Code Smells ที่พบในโค้ดเดิม (pricing_legacy.py)
**รายวิชา**: [31-407-102-302] วิศวกรรมซอฟต์แวร์ (Software Engineering) — Team 13  
**มาตรฐานอ้างอิง**: Refactoring: Improving the Design of Existing Code (Martin Fowler)  
**ไฟล์ที่ทำการวิเคราะห์**: `pricing_legacy.py` (แจกโดย อ.ดร.ปิยะนุช ตั้งกิตติพล)

---

## ตารางรายการ Code Smells (พบอย่างน้อย 6 ข้อตามเกณฑ์)

| # | ชื่อ Code Smell | จุดที่พบในโค้ด | อธิบายปัญหาและผลกระทบ |
|---|---|---|---|
| 1 | **Global State & Side Effects** | บรรทัด 8-9 (`member_points = {}`, `LOG = []`) | ฟังก์ชันมีการอ่านและแก้ไขตัวแปร Global โดยตรง (`member_points[member] = ...` และ `LOG.append(...)`) ส่งผลให้เกิด Hidden Side Effects และทำให้ Unit Test มีการแชร์ State ข้ามเคส รันเดี่ยวผ่านแต่รันรวมอาจพังได้ |
| 2 | **Magic Tuple Indices (Primitive Obsession)** | บรรทัด 18-24 (`i[1]`, `i[2]`) | รายการสินค้าถูกเก็บเป็น Tuple โดยไม่มีการระบุชื่อ Field ต้องเดาว่า `i[1]` คือจำนวน (`quantity`) และ `i[2]` คือราคาต่อหน่วย (`unit_price`) หากมีการสลับตำแหน่งข้อมูลจะเกิด Bug ทันที |
| 3 | **Magic Numbers** | บรรทัด 7, 21, 23, 29, 31, 41 (`0.07`, `100`, `0.9`, `50`, `0.95`, `0.8`) | ตัวเลขภาษี, ส่วนลดตามจำนวน, ส่วนลดสมาชิก และส่วนลดปีใหม่ ถูก Hardcode ไว้กระจายทั่วฟังก์ชัน ขาดชื่อตัวแปร Constants ทำให้แก้ไขและตรวจสอบนโยบายราคาได้ยาก |
| 4 | **Long Method & Low Cohesion** | บรรทัด 12-48 (ฟังก์ชัน `calc`) | ฟังก์ชันเดียวรับผิดชอบงานมากเกินไป (ขัดหลัก SRP) ทั้งวนลูปคิดราคาสินค้า, ลดตามจำนวน, คำนวณแต้มสมาชิก, ตรวจสอบคูปอง, ดึงวันปัจจุบัน, คิดภาษี, บันทึก Log และปัดเศษ |
| 5 | **Hidden Environmental / Time Dependency** | บรรทัด 38-39 (`datetime.date.today()`) | มีการเรียกวันที่ปัจจุบันจากระบบโดยตรงภายในฟังก์ชัน หากไม่ส่งพารามิเตอร์ `today` เข้ามา จะทำให้ผลลัพธ์ของคูปอง `NEWYEAR` ไม่สามารถทำนายผลได้ (Non-deterministic) และทดสอบแบบอัตโนมัติได้ยาก |
| 6 | **Non-idiomatic Comparison & Lack of Type Hints** | บรรทัด 26, 33, 38 (`member != None`, `coupon != None`) | การเปรียบเทียบกับ `None` ใน Python ควรใช้ `is not None` ตามมาตรฐาน PEP 8 รวมถึงไม่มี Type Hinting กำกับ signature ทำให้ผู้เรียกใช้งานคาดเดาประเภทข้อมูลผิดพลาด |

---

## สรุปแนวทางการ Refactor ในขั้นถัดไป
1. สร้าง Data Class `CartItem` หรือโครงสร้างที่อ่านง่าย แทนการใช้ Magic Indices `i[1]`, `i[2]`
2. แยก Business Logic ย่อยออกเป็นฟังก์ชันบริสุทธิ์ (Pure Functions): ส่วนลดจำนวน, ส่วนลดสมาชิก, ส่วนลดคูปอง และภาษี
3. นำ Global State (`member_points`, `LOG`) ออก แล้วส่งผ่าน Repository หรือ Return Value เพื่อให้ Testability สูงสุด
