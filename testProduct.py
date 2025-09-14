from model.product import Product

# Tạo các sản phẩm mẫu để kiểm tra
print("--- Thêm sản phẩm mẫu ---")
product1 = Product(
    name="Laptop XYZ", 
    price=1200.50, 
    rating=4.5, 
    image_url="http://example.com/laptop.jpg"
)
product1.save_product()
print("Đã thêm sản phẩm 1.")

product2 = Product(
    name="Điện thoại ABC", 
    price=750.00, 
    rating=4.8, 
    image_url="http://example.com/phone.jpg"
)
product2.save_product()
print("Đã thêm sản phẩm 2.")

# Gọi phương thức all_products() để lấy danh sách
print("\n--- Lấy tất cả sản phẩm từ cơ sở dữ liệu ---")
# Lưu ý: all_products là một phương thức của lớp, bạn có thể gọi nó trực tiếp từ lớp
all_products_list = Product.all_products() 

# In danh sách sản phẩm ra màn hình
print("--- In danh sách sản phẩm ---")
if all_products_list:
    for product in all_products_list:
        print(f"Tên: {product.name}")
        print(f"Giá: {product.price}")
        print(f"Đánh giá: {product.rating}")
        print(f"URL ảnh: {product.image_url}")
        print("-" * 20)
else:
    print("Không có sản phẩm nào trong cơ sở dữ liệu.")

#CẦN SỬA HÀM ALL_PRODUCTS(SELF) TRONG FILE PRODUCT.PY