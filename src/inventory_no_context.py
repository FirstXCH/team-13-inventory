class InventorySystem:
    def __init__(self):
        self.inventory = {}

    def add_product(self, product_id, name, stock, threshold, category, price):
        self.inventory[product_id] = {
            "name": name,
            "stock": stock,
            "threshold": threshold,
            "category": category,
            "price": price
        }
        print(f"เพิ่มสินค้า {name} สำเร็จ")

    def issue_product(self, product_id, amount):
        if product_id not in self.inventory:
            print("ไม่พบสินค้านี้ในระบบ")
            return

        item = self.inventory[product_id]
        if item["stock"] < amount:
            print("สต็อกไม่เพียงพอ")
            return

        item["stock"] -= amount
        print(f"จ่ายสินค้า {item['name']} จำนวน {amount} สำเร็จ สต็อกคงเหลือ {item['stock']}")

        # เช็คสต็อกต่ำและแจ้งเตือน
        if item["stock"] < item["threshold"]:
            print(f"ส่ง Email ถึง manager@store.com: สินค้า {item['name']} สต็อกต่ำกว่ากำหนด!")
            print(f"ส่ง SMS ถึง 0812345678: สินค้า {item['name']} สต็อกต่ำกว่ากำหนด!")

    def report_value_by_category(self, category):
        total_value = 0
        for item in self.inventory.values():
            if item["category"] == category:
                total_value += item["stock"] * item["price"]
        print(f"มูลค่ารวมของหมวด {category} คือ {total_value}")

# ทดสอบการทำงาน
if __name__ == "__main__":
    sys = InventorySystem()
    sys.add_product("P01", "สายไฟ 2.5 sq.mm", 20, 15, "อุปกรณ์ไฟฟ้า", 50)
    sys.issue_product("P01", 8)