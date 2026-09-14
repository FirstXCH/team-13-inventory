# 📦 Smart Inventory & E-Book Management System (Team 13)

[![SWE Inventory CI](https://github.com/FirstXCH/team-13-inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/FirstXCH/team-13-inventory/actions)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-6%20passed%20(100%25)-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/architecture-Clean%20%2F%203--Tier-orange.svg)](src/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

### 📋 ข้อมูลโครงงานและข้อมูลรายวิชา (Course & Team Info)
* **รหัสวิชา:** [31-407-102-302]
* **ชื่อวิชา:** วิศวกรรมซอฟต์แวร์ (Software Engineering) | หน่วยกิต: (2-1-3)
* **กลุ่มเรียน:** ECP3N | ห้องเรียน: ECP 321
* **อาจารย์ผู้สอน:** อาจารย์ ดร.ปิยะนุช ตั้งกิตติพล
* **ชื่อโครงงาน:** ระบบจัดการคลังสินค้าอัจฉริยะและหนังสือดิจิทัล (Smart Inventory Management System — Team 13)
* **ผู้จัดทำและผู้นำเสนอ:** นายกานต์นิธิ ยะโส รหัสนักศึกษา 67332110223-9 กลุ่ม ECP3N
* **โครงงานฐานข้อมูลที่เชื่อมโยง (Database Project):** ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (Lampara Books)
  * GitHub: [https://github.com/FirstXCH/BookSell-DatabaseProject](https://github.com/FirstXCH/BookSell-DatabaseProject)
  * Live Website: [https://lampara-books.vercel.app](https://lampara-books.vercel.app)

---

## 📖 คู่มือการอ่านทำความเข้าใจและเตรียมสอบ (Step-by-Step Study Guide)

เพื่อให้เข้าใจโครงงานอย่างครบถ้วนตามขั้นตอนวิศวกรรมซอฟต์แวร์ (Software Engineering Lifecycle) สามารถศึกษาเรียงตามขั้นตอน 8 ขั้นตอน ดังนี้:

| ขั้นตอน (Step) | เอกสารหลัก | รายละเอียดเนื้อหา | วัตถุประสงค์เพื่อการนำเสนอ |
|:---:|---|---|---|
| **STEP 01** | [**STEP_01: ภาพรวมโครงการและสถาปัตยกรรม**](STEP_01_ภาพรวมโครงการและสถาปัตยกรรม_PROJECT.md) | ที่มา ปัญหา ขอบเขตระบบ Clean Architecture และ 3-Tier Layer | อธิบายภาพรวม Business Domain และ High-Level Architecture |
| **STEP 02** | [**STEP_02: ข้อกำหนดความต้องการระบบ (SRS)**](STEP_02_ข้อกำหนดความต้องการระบบ_SRS.md) | Functional Requirements, Non-Functional, User Stories & Acceptance Criteria | ชี้แจงขอบเขตฟังก์ชันระบบและการวัดผลคุณภาพ |
| **STEP 03** | [**STEP_03: การออกแบบคลาสและโมเดล (Class Diagram)**](STEP_03_การออกแบบคลาสไดอะแกรม_CLASS_DIAGRAM.md) | UML Class Diagram, Sequence Diagram, Design Patterns (Observer, Strategy) | ตอบคำถามเรื่อง OOP, Polymorphism และการขยายระบบ |
| **STEP 04** | [**STEP_04: โครงสร้างโค้ดและการแยกเลเยอร์**](STEP_04_โครงสร้างโค้ดระบบ_SRC_CODE.md) | โค้ดใน src/ (models.py, service.py, 
otifiers.py), Separation of Concerns | อธิบายหลักการเขียนโค้ด การแยกหน้าที่ และ Dependency Inversion |
| **STEP 05** | [**STEP_05: การทดสอบระบบอัตโนมัติ (Tests)**](STEP_05_การทดสอบอัตโนมัติ_AUTOMATED_TESTS.md) | ชุดทดสอบ Pytest 6 กรณีทดสอบ (Boundary, Negative, Business Logic) ผ่าน 100% | สาธิตการทำ Automated Unit Testing และ CI/CD Pipeline |
| **STEP 06** | [**STEP_06: การออกแบบ UX และการเข้าถึง**](STEP_06_การออกแบบUXและการเข้าถึง_UX_ACCESSIBILITY.md) | Personas, User Journey, มาตรฐานการเข้าถึง WCAG 2.1 AA, Contrast Ratio | แสดงถึงความเข้าใจกลุ่มผู้ใช้งานและการออกแบบ Inclusive Design |
| **STEP 07** | [**STEP_07: บันทึกการใช้ AI และรีวิวระบบ**](STEP_07_บันทึกการใช้AIและรีวิวระบบ_AI_LOG_REVIEW.md) | Responsible AI Usage, AI Iteration Logs, Security Prompting & Guardrails | ตอบคำถามเรื่องการใช้ AI อย่างรับผิดชอบและตรวจสอบโค้ด |
| **STEP 08** | [**STEP_08: สรุปผลการทำงานเป็นทีมและสปรินต์**](STEP_08_สรุปผลการทำงานเป็นทีมและสปรินต์_RETRO_SPRINT.md) | Agile Scrum, Sprint Retrospective 1, Burn-down Chart, Action Items | สรุปผลการจัดการโครงงานและการปรับปรุงกระบวนการพัฒนา |

---

## 🏗️ สถาปัตยกรรมระบบและกฎทางธุรกิจ (Architecture & Business Logic)

ระบบ Inventory นี้ได้รับการออกแบบเชิงวัตถุ (Object-Oriented Design) เพื่อรองรับสินค้า 2 ประเภทที่มีกฎทางธุรกิจต่างกันโดยสิ้นเชิง:

`
                      +-------------------+
                      |   Base Product    |
                      |  (Abstract Class) |
                      +-------------------+
                                |
               +----------------+----------------+
               |                                 |
      +-------------------+             +-------------------+
      |  PhysicalProduct  |             |   DigitalProduct  |
      +-------------------+             +-------------------+
      | - stock: int      |             | - download_url    |
      | - threshold: int  |             | - access_status   |
      +-------------------+             +-------------------+
      | * ตัดสต็อกเมื่อขาย |             | * ไม่ตัดสต็อก     |
      | * ตรวจสอบ LowStock|             | * ล็อกลิงก์จนกว่า |
      | * ห้ามขายเกินสต็อก |             |   จะชำระเงินจริง  |
      +-------------------+             +-------------------+
`

### 1. สินค้าทางกายภาพ (Physical Goods: หนังสือรูปเล่ม)
* **การตัดสต็อก:** ทุกครั้งที่มีการสั่งซื้อ ระบบจะลดค่า stock ตามจำนวนที่ซื้อ
* **Validation:** หากจำนวนสั่งซื้อมากกว่าสต็อกคงเหลือ ระบบจะโยน ValueError('ยอดสต็อกไม่เพียงพอ')
* **Low Stock Observer:** เมื่อยอดคงเหลือต่ำกว่าหรือเท่ากับ 	hreshold ระบบจะส่งสัญญาณเตือนไปยัง InventoryNotifier ทันที

### 2. สินค้าดิจิทัล (Digital Goods: อีบุ๊ก/ไฟล์ PDF)
* **Zero Physical Stock:** สินค้าประเภทนี้ไม่มีวันหมดสต็อก (stock เป็น None) จึงไม่ถูกตัดยอด
* **Fulfillment & Access Control:** มีระบบความปลอดภัยควบคุมลิงก์ดาวน์โหลด โดยลิงก์จะถูก **ล็อก (Locked)** ในสถานะ Pending และจะปลดล็อกให้เข้าถึงไฟล์ได้เฉพาะเมื่อคำสั่งซื้อเป็น **Confirmed** เท่านั้น

---

## 🧪 การทดสอบระบบอัตโนมัติ (Automated Testing with Pytest)

ระบบมีชุดทดสอบอัตโนมัติครอบคลุม 6 Test Cases สำคัญตามเกณฑ์วิศวกรรมซอฟต์แวร์:

`ash
# ติดตั้ง pytest (หากยังไม่ได้ติดตั้ง)
pip install pytest

# รันชุดทดสอบพร้อมรายงานผลแบบละเอียด
pytest tests/ -v
`

### ผลการทดสอบ (Test Results: 100% Passed):
`	ext
============================= test session starts =============================
platform win32 -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\learnCode	eam-13-inventory
plugins: anyio-4.13.0
collected 6 items

tests/test_inventory.py::test_physical_product_stock_deduction PASSED    [ 16%]
tests/test_inventory.py::test_physical_product_cannot_sell_beyond_stock PASSED [ 33%]
tests/test_inventory.py::test_digital_product_no_stock_deduction PASSED  [ 50%]
tests/test_inventory.py::test_digital_product_download_locked_when_pending PASSED [ 66%]
tests/test_inventory.py::test_digital_product_download_unlocked_when_confirmed PASSED [ 83%]
tests/test_inventory.py::test_low_stock_notification PASSED              [100%]

============================== 6 passed in 0.02s ==============================
`

---

## 📁 โครงสร้างไดเรกทอรีของโครงงาน (Project Structure)

`
team-13-inventory/
├── .github/
│   └── workflows/
│       └── ci.yml                     # ระบบ CI/CD ทดสอบโค้ดอัตโนมัติบน GitHub Actions
├── diagrams/                          # แผนภาพการออกแบบระบบ
│   ├── class.md                       # UML Class Diagram (Mermaid)
│   └── sequence.md                    # Sequence Diagram
├── docs/                              # เอกสารคู่มือและการออกแบบ
│   ├── images/                        # ไฟล์รูปภาพประกอบ
│   │   └── sprint_board.png           # รูปภาพ Sprint Task Board & Burndown
│   ├── team/                          # เอกสารการจัดการทีม
│   │   ├── TEAM_CHARTER.md            # กฎบัตรทีมและบทบาทหน้าที่
│   │   ├── RETRO-SPRINT-1.md          # รายงานการประเมินผลสปรินต์ที่ 1
│   │   └── AI_ITERATION_LOG.md        # บันทึกการสร้างโค้ดด้วย AI
│   └── ux/                            # การออกแบบ UX และความพร้อมเข้าถึง
│       ├── accessibility.md           # การวิเคราะห์ WCAG 2.1 AA
│       └── persona.md                 # ข้อมูลกลุ่มเป้าหมายผู้ใช้งาน
├── specs/                             # ข้อกำหนดทางเทคนิค
│   └── spec.md                        # Software Requirements Specification
├── src/                               # ซอร์สโค้ดภาษา Python (Clean Architecture)
│   ├── models.py                      # โมเดลข้อมูล (PhysicalProduct, DigitalProduct)
│   ├── service.py                     # Business Logic (InventoryService)
│   ├── notifiers.py                   # แจ้งเตือน Low Stock (Observer Pattern)
│   └── inventory.py                   # Inventory Controller
├── tests/                             # ชุดทดสอบอัตโนมัติ
│   └── test_inventory.py              # Automated Unit Tests (6 Cases)
├── STEP_01_ภาพรวมโครงการและสถาปัตยกรรม_PROJECT.md
├── STEP_02_ข้อกำหนดความต้องการระบบ_SRS.md
├── STEP_03_การออกแบบคลาสไดอะแกรม_CLASS_DIAGRAM.md
├── STEP_04_โครงสร้างโค้ดระบบ_SRC_CODE.md
├── STEP_05_การทดสอบอัตโนมัติ_AUTOMATED_TESTS.md
├── STEP_06_การออกแบบUXและการเข้าถึง_UX_ACCESSIBILITY.md
├── STEP_07_บันทึกการใช้AIและรีวิวระบบ_AI_LOG_REVIEW.md
├── STEP_08_สรุปผลการทำงานเป็นทีมและสปรินต์_RETRO_SPRINT.md
├── .ai-rules.md                       # ข้อกำหนดการควบคุมการใช้ AI ในทีม
├── .gitignore                         # กำหนดไฟล์ที่ไม่ติดตามใน Git
└── README.md                          # เอกสารภาพรวมหลัก (หน้านี้)
`

---

## 👥 สมาชิกทีมและบทบาท (Team 13 Members & Roles)
* **นายกานต์นิธิ ยะโส (รหัสนักศึกษา 67332110223-9)**
  * **Role:** Scrum Master / Backend & Database Developer
  * **Responsibilities:** ออกแบบโครงสร้างระบบ, พัฒนา Core Inventory Logic, เขียน Automated Test Suites, ดูแล CI/CD และเอกสารวิศวกรรมซอฟต์แวร์
* ดูรายละเอียดสมาชิก กฎระเบียบทีม และข้อตกลงการทำงานได้ที่ [TEAM_CHARTER.md](docs/team/TEAM_CHARTER.md)

---
*จัดทำขึ้นสำหรับการศึกษาและส่งผลงานในรายวิชาวิศวกรรมซอฟต์แวร์ (Software Engineering) ปีการศึกษา 2026*
