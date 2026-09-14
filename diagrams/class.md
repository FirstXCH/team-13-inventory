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
