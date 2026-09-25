# โครงงานวิศวกรรมซอฟต์แวร์: ระบบจัดการคลังสินค้า (Smart Inventory System)
**ทีมพัฒนา**: Team 13  
**รายวิชา**: [31-407-201-101] วิศวกรรมซอฟต์แวร์ (Software Engineering)  
**อาจารย์ผู้สอน**: อ.ดร.ปิยะนุช ตั้งกิตติพล  
**หลักสูตร**: วิศวกรรมคอมพิวเตอร์ (ECP) ชั้นปีที่ 3 คณะวิศวกรรมศาสตร์ มทร.อีสาน  

---

## 1. แผนผังที่ตั้งไฟล์สำคัญใน Repository (File Directory Map)
เพื่อให้ผู้สอนสามารถตรวจประเมินตามเกณฑ์โครงงาน 20 คะแนน และงาน Lab 4-5 ได้อย่างสะดวกรวดเร็ว:

| หมวดหมู่การประเมิน | ตำแหน่งไฟล์ใน Repository | คำอธิบายสาระสำคัญ |
|---|---|---|
| **1. Spec & Acceptance Criteria (4 คะแนน)** | [`specs/spec.md`](specs/spec.md) | ขอบเขตระบบ, User Stories, และ Acceptance Criteria (Given-When-Then) |
| **2. Software Diagrams (4 คะแนน)** | [`diagrams/class.md`](diagrams/class.md)<br>[`diagrams/sequence.md`](diagrams/sequence.md)<br>[`diagrams/class.puml`](diagrams/class.puml)<br>[`diagrams/sequence.puml`](diagrams/sequence.puml) | Class Diagram และ Sequence Diagram (ไม่มีการส่ง ERD แทน Class Diagram) |
| **3. งานฝั่งผู้ใช้ UX & Accessibility (3 คะแนน)** | [`docs/ux/persona.md`](docs/ux/persona.md)<br>[`docs/ux/accessibility.md`](docs/ux/accessibility.md)<br>[`lab04-ai-coding-ux/`](lab04-ai-coding-ux/) | Persona ผู้ใช้จริง, Wireframe ASCII, ลิงก์ Mockup และผลตรวจ Accessibility |
| **4. Automated Test & CI (4 คะแนน)** | [`tests/test_inventory.py`](tests/test_inventory.py)<br>[`.github/workflows/ci.yml`](.github/workflows/ci.yml)<br>[`test-gap.md`](test-gap.md)<br>[`coverage-note.md`](coverage-note.md) | Unit Test รันผ่านจริง 17 เคส (TDD + Edge Cases) และ CI Actions รันผ่าน 100% |
| **5. บันทึก AI & จริยธรรม (3 คะแนน)** | [`docs/team/AI_ITERATION_LOG.md`](docs/team/AI_ITERATION_LOG.md)<br>[`ethics.md`](ethics.md) | ประวัติ Prompt, จุดที่ปฏิเสธข้อเสนอ AI พร้อมเหตุผล, และข้อปฏิบัติด้าน PDPA |
| **6. โค้ดระบบหลัก (Domain Logic)** | [`src/models.py`](src/models.py)<br>[`src/service.py`](src/service.py)<br>[`src/notifiers.py`](src/notifiers.py) | รองรับสินค้า 2 ชนิด (Physical ตัดสต็อก vs Digital สิทธิ์ดาวน์โหลด) |
| **7. ชิ้นงาน Lab 4 (UX, Review, Debug)** | [`lab04-ai-coding-ux/code-review.md`](lab04-ai-coding-ux/code-review.md)<br>[`lab04-ai-coding-ux/debug-log.md`](lab04-ai-coding-ux/debug-log.md) | บันทึกการรีวิว PR โค้ด AI และบันทึกการดีบักตามหลักฐาน 5 ขั้นตอน |
| **8. ชิ้นงาน Lab 5 (TDD, Refactor, CI)** | [`smells.md`](smells.md)<br>[`src/pricing.py`](src/pricing.py)<br>[`tests/test_pricing_legacy.py`](tests/test_pricing_legacy.py) | รายการ Code Smells, Characterization Tests และโค้ด Refactor |

---

## 2. ลิงก์คลิปวิดีโอสาธิตระบบ (3 ถึง 5 นาที)
* **ลิงก์วิดีโอบน YouTube / Google Drive**: `https://youtu.be/demo-team-13-inventory` *(เตรียมแปะลิงก์คลิปจริงที่สมาชิกทุกคนร่วมพูดนำเสนอ)*
* **โครงสร้างการนำเสนอในคลิป (ความยาว 3-5 นาที)**:
  1. *นาทีที่ 0:00 - 1:00*: แนะนำสมาชิกและภาพรวมสถาปัตยกรรมระบบ 2 สินค้า (Physical vs Digital)
  2. *นาทีที่ 1:01 - 2:30*: สาธิตการรันโค้ดจริง การตัดสต็อกสินค้ากายภาพ, การบล็อกดาวน์โหลดสินค้าดิจิทัลถ้ายังไม่ Confirmed, และระบบแจ้งเตือนสต็อกต่ำ
  3. *นาทีที่ 2:31 - 3:45*: แสดงผลการรัน Automated Unit Tests (17/17 passed) และการตรวจ CI บน GitHub Actions
  4. *นาทีที่ 3:46 - 4:45*: สรุปกระบวนการ Agile Scrum, บันทึกการใช้ AI แบบ Human-in-the-Loop และประเด็นจริยธรรม

---

## 3. ลิงก์เชื่อมโยงไปยังรายวิชาระบบฐานข้อมูล (Cross-Reference)
> ตามประกาศรายวิชาวิศวกรรมซอฟต์แวร์ วันที่ 12 ก.ย. เรื่องการแยก Repository:  
> งานระบบฐานข้อมูล (Mini Project Database: ERD, Data Dictionary, คำสั่ง SQL สร้างตาราง, และ Query Report) จัดเก็บแยกอยู่อีก Repository เพื่อไม่ให้ปะปนกับ Core Domain Logic ของวิชานี้ ที่:  
> **https://github.com/FirstXCH/BookSell-DatabaseProject**
