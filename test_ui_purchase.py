import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# Cấu hình Trình duyệt (Fixture)
# Fixture này giúp khởi tạo trình duyệt trước khi test và đóng nó sau khi test xong
# ==========================================
@pytest.fixture(scope="function")
def driver():
    # 1. Thiết lập các tùy chọn cho Chrome
    chrome_options = Options()
    
    # CHÚ Ý QUAN TRỌNG CHO CI/CD: 
    # Bắt buộc bật headless để chạy trên máy ảo GitHub không có màn hình
    chrome_options.add_argument("--headless") 
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Đặt kích thước cửa sổ chuẩn để các phần tử không bị ẩn
    chrome_options.add_argument("--window-size=1920,1080") 

    # 2. Tự động tải và cài đặt ChromeDriver tương thích
    service = Service(ChromeDriverManager().install())
    
    # 3. Khởi tạo trình duyệt Chrome với các cấu hình trên
    web_driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Thiết lập thời gian chờ ngầm định (Implicit Wait) là 10 giây
    # Nếu không tìm thấy phần tử, nó sẽ đợi tối đa 10s trước khi báo lỗi.
    web_driver.implicitly_wait(10)
    
    yield web_driver # Trả trình duyệt về cho hàm test sử dụng
    
    # 4. Đóng trình duyệt sau khi test xong (Teardown)
    # time.sleep(2) # Bật dòng này nếu muốn nó dừng 2s cho bạn kịp nhìn kết quả
    web_driver.quit()

# ==========================================
# TEST CASE: Luồng mua hàng hoàn chỉnh (End-to-End UI Test)
# Scenario: Login -> Add Item -> Go to Cart -> Checkout -> Finish
# Site: https://www.saucedemo.com/
# ==========================================
def test_end_to_end_ui_purchase_flow(driver):
    # Bước 1: Mở trang web
    print("\n[UI Test] Dang mo trang web Swag Labs...")
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title # Kiểm tra tiêu đề trang web
    
    # Bước 2: Đăng nhập (Dùng tài khoản standard_user có sẵn trên web)
    print("[UI Test] Dang thuc hien dang nhap...")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Kiểm tra đã vào được trang sản phẩm chưa
    assert "/inventory.html" in driver.current_url
    
    # Bước 3: Thêm sản phẩm đầu tiên vào giỏ hàng
    print("[UI Test] Dang them san pham 'Sauce Labs Backpack' vao gio hàng...")
    # Tìm nút 'Add to cart' của sản phẩm đầu tiên
    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) button")
    add_to_cart_btn.click()
    
    # Kiểm tra badge trên giỏ hàng có hiện số 1 không
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1"
    
    # Bước 4: Đi đến giỏ hàng
    print("[UI Test] Dang di den gio hang...")
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert "/cart.html" in driver.current_url
    # Kiểm tra tên sản phẩm trong giỏ hàng có đúng không
    cart_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert cart_item_name.text == "Sauce Labs Backpack"
    
    # Bước 5: Tiến hành Checkout (Thanh toán)
    print("[UI Test] Dang tien hanh Checkout...")
    driver.find_element(By.ID, "checkout").click()
    
    # Điền thông tin người mua (Điền đại thông tin)
    driver.find_element(By.ID, "first-name").send_keys("Ngoc")
    driver.find_element(By.ID, "last-name").send_keys("Tester")
    driver.find_element(By.ID, "postal-code").send_keys("10000")
    driver.find_element(By.ID, "continue").click()
    
    # Bước 6: Hoàn tất đơn hàng
    print("[UI Test] Dang xác nhan va hoan tat don hàng...")
    assert "/checkout-step-two.html" in driver.current_url
    driver.find_element(By.ID, "finish").click()
    
    # Bước 7: Xác nhận kết quả cuối cùng (Màn hình THANK YOU)
    assert "/checkout-complete.html" in driver.current_url
    complete_header = driver.find_element(By.CLASS_NAME, "complete-header")
    assert complete_header.text == "Thank you for your order!"
    print("[UI Test] => Test Case E2E UI PASSED ruc ro!")