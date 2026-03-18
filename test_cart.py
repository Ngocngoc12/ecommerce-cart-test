# test_cart.py
import pytest
from cart import ShoppingCart, InventoryDB
from unittest.mock import MagicMock

# ==========================================
# 1. UNIT TEST (Kiểm thử Mức Đơn Vị)
# Mục đích: Kiểm tra một hàm/method độc lập, cách ly hoàn toàn với các hệ thống khác.
# ==========================================
def test_get_total_empty_cart():
    cart = ShoppingCart()
    assert cart.get_total() == 0, "Giỏ hàng trống phải có tổng tiền là 0"

def test_get_total_with_items():
    cart = ShoppingCart()
    cart.items = [{"name": "Laptop", "price": 1000}, {"name": "Mouse", "price": 50}]
    assert cart.get_total() == 1050, "Tổng tiền tính toán bị sai"

# ==========================================
# 2. INTEGRATION TEST (Kiểm thử Tích Hợp)
# Mục đích: Kiểm tra sự giao tiếp giữa các module (Cart giao tiếp với InventoryDB).
# ==========================================
def test_add_item_integration_with_db():
    # Sử dụng DB thật (InventoryDB) để xem Cart có giao tiếp đúng không
    db = InventoryDB()
    cart = ShoppingCart(db)
    
    # Laptop có trong DB -> Phải thêm thành công
    assert cart.add_item("Laptop", 1000) is True
    
    # Bàn phím không có trong DB -> Phải thất bại
    assert cart.add_item("Keyboard", 100) is False

# ==========================================
# 3. FUNCTIONAL TEST (Kiểm thử Chức Năng)
# Mục đích: Kiểm tra xem hệ thống có đáp ứng đúng yêu cầu nghiệp vụ (Business Requirement) không.
# ==========================================
def test_apply_discount_percentage():
    cart = ShoppingCart()
    cart.items = [{"name": "Laptop", "price": 1000}]
    
    # Nghiệp vụ: Mã TESTER10 giảm 10%
    discounted_price = cart.apply_discount("TESTER10")
    assert discounted_price == 900, "Mã giảm giá 10% hoạt động không đúng"

def test_apply_invalid_discount():
    cart = ShoppingCart()
    cart.items = [{"name": "Laptop", "price": 1000}]
    
    # Nghiệp vụ: Mã sai thì giữ nguyên giá
    discounted_price = cart.apply_discount("WRONGCODE")
    assert discounted_price == 1000, "Mã sai nhưng hệ thống vẫn trừ tiền"

# ==========================================
# 4. SYSTEM TEST / E2E TEST (Kiểm thử Hệ Thống)
# Mục đích: Kiểm tra toàn bộ luồng hệ thống từ góc độ người dùng (End-to-End).
# Trong thực tế, E2E Test thường dùng Selenium/Playwright mở trình duyệt. 
# Ở đây ta mô phỏng một kịch bản API System test hoàn chỉnh.
# ==========================================
def test_end_to_end_purchase_flow():
    # Bước 1: Khởi tạo toàn bộ hệ thống
    cart = ShoppingCart()
    
    # Bước 2: Người dùng thêm 2 sản phẩm (1 có hàng, 1 hết hàng)
    cart.add_item("Laptop", 1000)  # Thành công
    cart.add_item("Monitor", 500)  # Thất bại (hết hàng)
    
    # Bước 3: Kiểm tra giỏ hàng chỉ chứa đúng 1 món
    assert len(cart.items) == 1
    assert cart.get_total() == 1000
    
    # Bước 4: Người dùng nhập mã freeship và tiến hành thanh toán
    final_checkout_price = cart.apply_discount("FREESHIP")
    
    # Bước 5: Xác nhận kết quả cuối cùng của hệ thống
    assert final_checkout_price == 985, "Luồng thanh toán E2E bị lỗi"