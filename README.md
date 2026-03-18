# 🛒 E-commerce Cart - Test Automation Project

![CI/CD Status](https://github.com/Ngocngoc12/ecommerce-cart-test/actions/workflows/python-tests.yml/badge.svg)

## 📌 Giới thiệu dự án
Đây là một dự án mô phỏng quá trình kiểm thử tự động (Automation Testing) cho tính năng Giỏ hàng Thương mại điện tử. Dự án được xây dựng nhằm mục đích minh họa việc áp dụng các mức độ kiểm thử phần mềm khác nhau trong thực tế, từ mức đơn vị (Unit) đến mức hệ thống (System/E2E).

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python 3.11
* **Testing Framework:** Pytest
* **CI/CD:** GitHub Actions (Tự động chạy test khi có code mới)
* **Khác:** Mocking (`unittest.mock`)

## 🎯 Các mức độ kiểm thử đã áp dụng

Trong dự án này, mình đã phân chia cấu trúc Test Case theo mô hình Kim tự tháp kiểm thử (Testing Pyramid):

1. **Unit Test (Kiểm thử mức đơn vị):** * Đảm bảo các hàm tính toán cơ bản (như tính tổng tiền giỏ hàng) hoạt động chính xác một cách độc lập.
2. **Integration Test (Kiểm thử tích hợp):** * Kiểm tra luồng giao tiếp giữa module `ShoppingCart` và giả lập cơ sở dữ liệu `InventoryDB` (Kho hàng).
3. **Functional Test (Kiểm thử chức năng):** * Xác minh các quy tắc nghiệp vụ (Business Logic) như áp dụng mã giảm giá phần trăm hoặc miễn phí vận chuyển.
4. **System/E2E Test (Kiểm thử hệ thống):** * Mô phỏng một kịch bản hoàn chỉnh của người dùng: Thêm sản phẩm (có sẵn/hết hàng) -> Áp dụng mã giảm giá -> Kiểm tra tổng tiền thanh toán cuối cùng.

## 🚀 Cách chạy dự án trên máy cá nhân (Local)

**1. Clone dự án về máy:**
```bash
git clone [https://github.com/Ngocngoc12/ecommerce-cart-test.git](https://github.com/Ngocngoc12/ecommerce-cart-test.git)
