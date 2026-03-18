# cart.py

class InventoryDB:
    """Giả lập Database kiểm tra số lượng hàng tồn kho"""
    def check_stock(self, item_name):
        # Giả sử trong kho luôn có 'Laptop' và 'Mouse', các món khác hết hàng
        stock = {"Laptop": 5, "Mouse": 10}
        return stock.get(item_name, 0) > 0

class ShoppingCart:
    def __init__(self, db=None):
        self.items = []
        self.db = db or InventoryDB() # Kết nối với Database kho hàng

    def add_item(self, item_name, price):
        """Thêm sản phẩm vào giỏ (chỉ thêm nếu còn hàng)"""
        if self.db.check_stock(item_name):
            self.items.append({"name": item_name, "price": price})
            return True
        return False

    def get_total(self):
        """Tính tổng tiền"""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, promo_code):
        """Áp dụng mã giảm giá (Functional logic)"""
        total = self.get_total()
        if promo_code == "TESTER10":
            return total * 0.9 # Giảm 10%
        elif promo_code == "FREESHIP":
            return total - 15 # Trừ 15k phí ship
        return total