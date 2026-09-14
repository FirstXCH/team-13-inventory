# 📐 STEP 03: การออกแบบคลาสไดอะแกรมและซีเควนซ์ไดอะแกรม (OOP Design)

> ⚠️ **คำสั่งสำคัญของ อ.ดร.ปิยะนุช:** ห้ามส่ง ER Diagram เด็ดขาด ต้องส่ง Class Diagram ที่แสดงความสัมพันธ์เชิงวัตถุ (Inheritance, Attributes, Methods)

---

# Class Diagram: ระบบจัดการคลังสินค้า (Inventory System)
รองรับสินค้า 2 ชนิด (Physical Goods & Digital Goods) และการแจ้งเตือนตามหลัก SOLID

```mermaid
classDiagram
    class Notifier {
        <<interface>>
        +send(message: str) None
    }
    class EmailNotifier {
        +send(message: str) None
    }
    class SMSNotifier {
        +send(message: str) None
    }
    class NotifierFactory {
        +create(channel: str) Notifier$
    }
    
    class Product {
        <<abstract>>
        +str id
        +str name
        +float price
        +str category
        +bool is_active
    }
    
    class PhysicalProduct {
        +int stock
        +int threshold
        +deduct_stock(quantity: int) bool
        +is_low_stock() bool
    }
    
    class DigitalProduct {
        +str file_url
        +str file_format
        +can_access_download(order_status: str) bool
    }
    
    class InventoryService {
        +Dict products
        -List~Notifier~ _observers
        +add_observer(observer: Notifier) None
        +add_product(product: Product) None
        +sell_product(product_id: str, quantity: int, order_status: str) dict
        +get_stock_value() float
        -_notify(message: str) None
    }
    
    Product <|-- PhysicalProduct : Inheritance (สินค้าจับต้องได้ ตัดสต็อก)
    Product <|-- DigitalProduct : Inheritance (สินค้าดิจิทัล ไม่ตัดสต็อก)
    Notifier <|.. EmailNotifier : Realization
    Notifier <|.. SMSNotifier : Realization
    NotifierFactory ..> Notifier : Creates (Factory Pattern)
    InventoryService o-- Notifier : Observer Pattern (Dependency Inversion)
    InventoryService o-- Product : Manages
```

## เหตุผลการออกแบบตามหลัก Software Engineering
1. **Open/Closed Principle (OCP)**: สามารถขยายชนิดสินค้าใหม่ได้ (เช่น สินค้าบริการ Subscription) โดยการสืบทอดจาก `Product` โดยไม่ต้องแก้โค้ดคำนวณเดิม
2. **Dependency Inversion Principle (DIP)**: `InventoryService` ขึ้นกับ `Notifier` Interface ไม่ได้ผูกติดกับ Email หรือ SMS โดยตรง
3. **Single Responsibility Principle (SRP)**: แยกการประมวลผลสต็อก (`PhysicalProduct`) ออกจากการตรวจสอบสิทธิ์ดาวน์โหลดไฟล์ (`DigitalProduct`)


---

# Sequence Diagram: กระบวนการขายและการจัดการสินค้า 2 ชนิด

```mermaid
sequenceDiagram
    actor Client as ผู้ใช้ระบบ / ลูกค้า
    participant Service as InventoryService
    participant Phys as PhysicalProduct
    participant Dig as DigitalProduct
    participant Observer as Notifier (Email/SMS)

    %% กรณีที่ 1: การขายสินค้าจริง (Physical Product)
    Note over Client, Phys: 1. กรณีขายสินค้าที่จับต้องได้ (Physical Goods)
    Client->>Service: sell_product("BOOK-P01", quantity=3)
    Service->>Phys: deduct_stock(3)
    Phys-->>Service: สำเร็จ (stock ลดลงจาก 10 เหลือ 7)
    Service->>Phys: is_low_stock()
    alt สต็อกต่ำกว่าเกณฑ์ threshold
        Service->>Observer: send("เตือน: สินค้าใกล้หมด")
    end
    Service-->>Client: ส่งคืนผลการขาย (ตัดสต็อกแล้ว)

    %% กรณีที่ 2: การขายสินค้าดิจิทัล (Digital Product)
    Note over Client, Dig: 2. กรณีขายสินค้าดิจิทัล (Digital Goods / E-Book)
    Client->>Service: sell_product("EBOOK-D01", quantity=1, order_status="Confirmed")
    Service->>Dig: can_access_download("Confirmed")
    Dig-->>Service: True (อนุมัติสิทธิ์ดาวน์โหลด)
    Note over Service, Dig: ไม่มีการตัดสต็อก (No Stock Deduction)
    Service-->>Client: ส่งคืนลิงก์ดาวน์โหลดไฟล์ (Download URL Unlocked)
```


---

## ?? ??????????????????????? PlantUML (`.puml`)
* **Class Diagram PlantUML:** [`diagrams/class.puml`](diagrams/class.puml)
* **Sequence Diagram PlantUML:** [`diagrams/sequence.puml`](diagrams/sequence.puml)

```plantuml
@startuml ClassDiagram_InventorySystem
title ???????????????????? (Smart Inventory Management System - Team 13)\n???????????? 2 ???? (Physical Goods & Digital Goods) ?????????????????????? SOLID

skinparam classAttributeIconSize 0
skinparam monochrome false
skinparam shadowing true
skinparam packageStyle rectangle

interface Notifier {
    +send(message: str): None
}

class EmailNotifier implements Notifier {
    +send(message: str): None
}

class SMSNotifier implements Notifier {
    +send(message: str): None
}

class NotifierFactory {
    +{static} create(channel: str): Notifier
}

abstract class Product {
    +id: str
    +name: str
    +price: float
    +category: str
    +is_active: bool
}

class PhysicalProduct extends Product {
    +stock: int
    +threshold: int
    +deduct_stock(quantity: int): bool
    +is_low_stock(): bool
}

class DigitalProduct extends Product {
    +file_url: str
    +file_format: str
    +can_access_download(order_status: str): bool
}

class InventoryService {
    +products: dict
    -_observers: list<Notifier>
    +add_observer(observer: Notifier): None
    +add_product(product: Product): None
    +sell_product(product_id: str, quantity: int, order_status: str): dict
    +get_stock_value(): float
    -_notify(message: str): None
}

NotifierFactory ..> Notifier : creates
InventoryService o-- Notifier : observer pattern
InventoryService o-- Product : manages

note bottom of PhysicalProduct
  <b>Physical Goods</b>
  - ????????????????
  - ????????????????????? threshold
  - ???????????????? (ValueError)
end note

note bottom of DigitalProduct
  <b>Digital Goods (E-Book)</b>
  - ????????????? (Zero Physical Stock)
  - ???????????????? (Access Control)
  - ??????????????????? status = 'Confirmed'
end note

@enduml

```
