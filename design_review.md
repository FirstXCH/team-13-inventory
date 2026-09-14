# การตรวจสอบหลักการออกแบบ (SOLID Design Review)

จากการตรวจสอบโค้ดในไฟล์ `service.py` และ `notifiers.py` พบประเด็นดังนี้:

| หลัก SOLID | ละเมิดหรือไม่ | จุดที่เกี่ยวข้อง (class/method) | อธิบาย/ผลกระทบ | ข้อเสนอปรับปรุง |
| --- | --- | --- | --- | --- |
| **S (SRP)** | ละเมิด | `InventoryService.issue_product` | เมธอดนี้ทำหน้าที่ 2 อย่างคือ 1) หักลบสต็อก (Business Logic) และ 2) จัดการเงื่อนไขการส่งแจ้งเตือน (Notification Logic) ทำให้คลาสมีภาระเยอะเกินไป | ควรแยกส่วนการแจ้งเตือนออกไปให้ Notifier จัดการตัวเอง หรือใช้ Observer Pattern |
| **O (OCP)** | ละเมิด | `InventoryService.issue_product` | มีการใช้ `if channel == "email": ... elif channel == "sms":` ถ้าอนาคตมีแจ้งเตือนทาง Line หรือ Slack ต้องกลับมาแก้โค้ดที่ไฟล์นี้เรื่อยๆ | เปลี่ยนไปใช้ Factory Pattern ในการสร้าง Notifier เพื่อให้รองรับช่องทางใหม่ๆ ได้โดยไม่ต้องแก้โค้ดเดิม |
| **L (LSP)** | ไม่ละเมิด | `EmailNotifier`, `SMSNotifier` | ปัจจุบัน Notifier ทั้งสองตัวมีโครงสร้างเมธอด `send()` เหมือนกัน แต่ยังไม่มีการสืบทอดจาก Class หลัก (Interface) ที่ชัดเจน | ควรสร้าง Base Class หรือ Protocol กลางให้ Notifier ทุกตัวใช้โครงสร้างเดียวกัน |
| **I (ISP)** | ไม่ละเมิด | `EmailNotifier`, `SMSNotifier` | คลาส Notifier มีแค่เมธอด `send()` เมธอดเดียว ไม่ได้มี Interface ที่ใหญ่หรือซับซ้อนเกินไปจนคลาสลูกไม่ได้ใช้ | (คงไว้ตามเดิม) |
| **D (DIP)** | ละเมิด | `InventoryService.__init__` | Service มีการ import และสร้าง object `EmailNotifier()` และ `SMSNotifier()` ตรงๆ (ผูกติดกับ Concrete Class) | Service ควรรับตัว Notifier เข้ามาผ่าน Constructor (Dependency Injection) หรือ Factory แทนการสร้างเอง |