# 1. ข้อมูลจำลองสินค้า (List of Dictionaries)
inventory = [
    {"id": "P001", "name": "Keyboard", "quantity": 10},
    {"id": "P002", "name": "Mouse", "quantity": 25},
    {"id": "P003", "name": "Monitor", "quantity": 5},
]

print("=== ยินดีต้อนรับสู่ระบบจัดการคลังสินค้า ===")
print("คำสั่งที่ใช้งานได้: 'list' (ดูรายการสินค้า), 'exit' (ออกจากโปรแกรม)")

# 2. Main Loop รับคำสั่งจากผู้ใช้แบบ Interactive
while True:
    command = input("\nกรุณาใส่คำสั่ง: ").strip().lower()

    # 3. จัดการคำสั่ง 'list' เพื่อแสดงรายการสินค้า
    if command == "list":
        # ตรวจสอบว่ามีสินค้าในระบบหรือไม่
        if not inventory:
            print("ยังไม่มีสินค้าในระบบ")
        else:
            print("\n--- รายการสินค้าคงเหลือ ---")
            print(f"{'รหัสสินค้า':<10} | {'ชื่อสินค้า':<15} | {'จำนวนคงเหลือ'}")
            print("-" * 42)
            for item in inventory:
                print(f"{item['id']:<10} | {item['name']:<15} | {item['quantity']}")

    # 4. จัดการคำสั่ง 'exit' เพื่อจบการทำงาน
    elif command == "exit":
        print("ปิดการทำงานของโปรแกรมเรียบร้อยแล้ว")
        break

    # กรณีผู้ใช้พิมพ์คำสั่งอื่นที่ไม่ถูกต้อง
    else:
        print("คำสั่งไม่ถูกต้อง กรุณาพิมพ์ 'list' หรือ 'exit'")