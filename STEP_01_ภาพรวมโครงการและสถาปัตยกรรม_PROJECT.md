# โครงงานวิศวกรรมซอฟต์แวร์: ระบบคลังสินค้า (Inventory Management System)
**ทีมพัฒนา**: Team 13  
**รายวิชา**: [31-407-201-101] วิศวกรรมซอฟต์แวร์ (Software Engineering)  
**อาจารย์ผู้สอน**: อ.ดร.ปิยะนุช ตั้งกิตติพล  
**หลักสูตร**: วิศวกรรมคอมพิวเตอร์ (ECP) ชั้นปีที่ 3 คณะวิศวกรรมศาสตร์ มทร.อีสาน  

---

## 1. แผนผังที่ตั้งไฟล์สำคัญใน Repository (File Directory Map)
เพื่อให้ผู้สอนสามารถตรวจประเมินตามเกณฑ์ 20 คะแนนได้อย่างสะดวก รวดเร็ว และเป็นระบบ:

| หมวดหมู่การประเมิน | ตำแหน่งไฟล์ใน Repository | คำอธิบายสาระสำคัญ |
|---|---|---|
| **1. Spec & User Story (4 คะแนน)** | [`specs/spec.md`](specs/spec.md) | ขอบเขตระบบ, User Stories, และ Acceptance Criteria (Given-When-Then) |
| **2. Software Diagrams (4 คะแนน)** | [`diagrams/class.md`](diagrams/class.md)<br>[`diagrams/sequence.md`](diagrams/sequence.md) | Class Diagram และ Sequence Diagram (ไม่มีการส่ง ERD แทน Class Diagram) |
| **3. งานฝั่งผู้ใช้ UX (3 คะแนน)** | [`docs/ux/persona.md`](docs/ux/persona.md)<br>[`docs/ux/accessibility.md`](docs/ux/accessibility.md) | Persona ผู้ใช้ และผลตรวจ Accessibility พร้อมจุดแก้เป็นข้อๆ |
| **4. Automated Test & CI (4 คะแนน)** | [`tests/test_inventory.py`](tests/test_inventory.py)<br>[`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Unit Test รันผ่านจริง 6 เคส และ GitHub Actions CI รันบน Pull Request |
| **5. บันทึก AI & จริยธรรม (3 คะแนน)** | [`AI_ITERATION_LOG.md`](AI_ITERATION_LOG.md) | บันทึก Prompt, จุดที่ปฏิเสธข้อเสนอ AI พร้อมเหตุผล, และประเด็น PDPA |
| **6. โค้ดระบบหลัก** | [`src/models.py`](src/models.py)<br>[`src/service.py`](src/service.py)<br>[`src/notifiers.py`](src/notifiers.py) | รองรับสินค้า 2 ชนิด (Physical ตัดสต็อก vs Digital ล็อกดาวน์โหลด) |

---

## 2. ลิงก์คลิปวิดีโอสาธิตระบบ (3 ถึง 5 นาที)
* **ลิงก์วิดีโอบน YouTube / Google Drive**: `https://youtu.be/demo-team-13-inventory` *(เตรียมแปะลิงก์คลิปที่สมาชิกทุกคนพูด)*
* **สรุปเนื้อหาในคลิป**: แสดงการทำงานของโค้ดจริง, การตัดสต็อกสินค้าจริง, การห้ามขายเกินสต็อก, การล็อก/ปลดล็อกดาวน์โหลดสินค้าดิจิทัล, และการรัน Unit Test ผ่าน CI

---

## 3. ลิงก์เชื่อมโยงไปยังรายวิชาระบบฐานข้อมูล (Cross-Reference)
> งานระบบฐานข้อมูล (Mini Project Database) ของรายวิชาระบบฐานข้อมูล จัดเก็บแยกอยู่ที่ Repository:  
> **https://github.com/FirstXCH/BookSell-DatabaseProject**
