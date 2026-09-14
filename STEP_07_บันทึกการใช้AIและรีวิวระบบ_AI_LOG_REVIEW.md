# 🤖 STEP 07: บันทึกการประยุกต์ใช้ AI (AI Iteration Log) และการรีวิวสถาปัตยกรรม (Design Review)

# บันทึกการใช้งานปัญญาประดิษฐ์ (AI Usage & Iteration Log)
**รายวิชา**: วิศวกรรมซอฟต์แวร์ (Software Engineering) — Team 13

---

## 1. ตารางบันทึกการส่ง Prompt และผลลัพธ์
| วันที่ | เครื่องมือ | Prompt สรุป | ผลลัพธ์ที่ได้ | การตรวจทานโดยทีม |
|---|---|---|---|---|
| 16 ส.ค. 69 | Claude / Antigravity | ออกแบบ Class Diagram และ SOLID Refactor สำหรับคลังสินค้า | แนะนำแยก Service, Model และ Notifier | นำมาปรับใช้ร่วมกับ Observer และ Factory Pattern |
| 11 ก.ย. 69 | Claude / Antigravity | ช่วยเขียน Unit Test ครอบคลุมกฎ 2 ชนิดสินค้า (Physical vs Digital) | ได้โครงสร้างเทส 6 ฟังก์ชัน | ตรวจทาน Assertions รันผ่านจริงบน pytest 100% |
| 14 ก.ย. 69 | Claude / Antigravity | ช่วยทำ Accessibility Audit Checklist ตามมาตรฐาน WCAG 2.1 | ได้ตารางประเมิน 4 มิติ | ปรับปรุง Contrast และ aria-label ใน UI |

---

## 2. จุดที่ทีมตัดสินใจ "ไม่ทำตามข้อเสนอของ AI" พร้อมเหตุผล (Rejected AI Proposals)
1. **AI เสนอให้ใช้สต็อกจำลอง (Stock = 999) สำหรับสินค้าดิจิทัล**:
   - *เหตุผลที่ปฏิเสธ*: เป็นการออกแบบที่ไม่ตรงตามหลัก OOP และขัดต่อกฎประกาศ 11 ก.ย. สินค้าดิจิทัลต้องไม่มีสต็อกให้ตัด ทีมจึงปฏิเสธและออกแบบคลาส `DigitalProduct` แยกออกมาโดยไม่มีฟิลด์ stock
2. **AI เสนอให้เปิดลิงก์ดาวน์โหลดทันทีเมื่อลูกค้ากดสั่งซื้อ โดยไม่ต้องรอการชำระเงิน**:
   - *เหตุผลที่ปฏิเสธ*: เสี่ยงต่อความเสียหายทางธุรกิจอย่างรุนแรง ทีมจึงปฏิเสธและบังคับใช้กฎ `order_status in ['Confirmed', 'Completed', 'Paid']` เท่านั้น
3. **AI เสนอให้คัดลอกไฟล์ SQL และ ERD จากวิชา Database มาใส่ใน Repo นี้**:
   - *เหตุผลที่ปฏิเสธ*: ขัดต่อประกาศวันที่ 12 ก.ย. ข้อ 1 และข้อ 6 ซึ่ง อ.ปิยะนุช สั่งห้ามนำ ERD และ SQL มารวมใน Repo นี้โดยเด็ดขาด ให้แยก 2 Repositories และเชื่อมด้วยลิงก์ 1 บรรทัดเท่านั้น

---

## 3. ประเด็นจริยธรรมข้อมูลส่วนบุคคล (PDPA Consideration)
ระบบไม่บันทึกข้อมูลส่วนบุคคลที่ละเอียดอ่อน (Sensitive Data) หรือรหัสผ่านแบบ Plain Text ข้อมูลจำลองในระบบทั้งหมดเป็นข้อมูลสมมุติ ไม่ละเมิดสิทธิส่วนบุคคลของลูกค้า


---

# การตรวจสอบหลักการออกแบบ (SOLID Design Review)

จากการตรวจสอบโค้ดในไฟล์ `service.py` และ `notifiers.py` พบประเด็นดังนี้:

| หลัก SOLID | ละเมิดหรือไม่ | จุดที่เกี่ยวข้อง (class/method) | อธิบาย/ผลกระทบ | ข้อเสนอปรับปรุง |
| --- | --- | --- | --- | --- |
| **S (SRP)** | ละเมิด | `InventoryService.issue_product` | เมธอดนี้ทำหน้าที่ 2 อย่างคือ 1) หักลบสต็อก (Business Logic) และ 2) จัดการเงื่อนไขการส่งแจ้งเตือน (Notification Logic) ทำให้คลาสมีภาระเยอะเกินไป | ควรแยกส่วนการแจ้งเตือนออกไปให้ Notifier จัดการตัวเอง หรือใช้ Observer Pattern |
| **O (OCP)** | ละเมิด | `InventoryService.issue_product` | มีการใช้ `if channel == "email": ... elif channel == "sms":` ถ้าอนาคตมีแจ้งเตือนทาง Line หรือ Slack ต้องกลับมาแก้โค้ดที่ไฟล์นี้เรื่อยๆ | เปลี่ยนไปใช้ Factory Pattern ในการสร้าง Notifier เพื่อให้รองรับช่องทางใหม่ๆ ได้โดยไม่ต้องแก้โค้ดเดิม |
| **L (LSP)** | ไม่ละเมิด | `EmailNotifier`, `SMSNotifier` | ปัจจุบัน Notifier ทั้งสองตัวมีโครงสร้างเมธอด `send()` เหมือนกัน แต่ยังไม่มีการสืบทอดจาก Class หลัก (Interface) ที่ชัดเจน | ควรสร้าง Base Class หรือ Protocol กลางให้ Notifier ทุกตัวใช้โครงสร้างเดียวกัน |
| **I (ISP)** | ไม่ละเมิด | `EmailNotifier`, `SMSNotifier` | คลาส Notifier มีแค่เมธอด `send()` เมธอดเดียว ไม่ได้มี Interface ที่ใหญ่หรือซับซ้อนเกินไปจนคลาสลูกไม่ได้ใช้ | (คงไว้ตามเดิม) |
| **D (DIP)** | ละเมิด | `InventoryService.__init__` | Service มีการ import และสร้าง object `EmailNotifier()` และ `SMSNotifier()` ตรงๆ (ผูกติดกับ Concrete Class) | Service ควรรับตัว Notifier เข้ามาผ่าน Constructor (Dependency Injection) หรือ Factory แทนการสร้างเอง |