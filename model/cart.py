# model/cart.py
from model.product import get_all_products, get_product_by_id

MOCK_CART = []
MOCK_WISHLIST = []
APPLIED_VOUCHER = None

def get_cart_details():
    """Lấy thông tin chi tiết giỏ hàng để hiển thị"""
    products = get_all_products()
    cart_items = []
    subtotal = 0
    
    for item in MOCK_CART:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if product:
            total_price = product['price'] * item['qty']
            subtotal += total_price
            cart_items.append({
                "product": product,
                "qty": item['qty'],
                "variant_name": item.get('variant_name', ''),
                "total_price": total_price
            })

    # Tính phí ship
    shipping_fee = 30000 if subtotal < 5000000 and subtotal > 0 else 0
    
    # Tính voucher
    discount = 0
    if APPLIED_VOUCHER == 'GIAM10':
        discount = subtotal * 0.1 
    
    final_total = subtotal + shipping_fee - discount

    return {
        "items": cart_items,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "discount": discount,
        "final_total": final_total,
        "voucher": APPLIED_VOUCHER
    }

def add_to_cart(product_id, qty=1, variant_id=None):
    """EPIC 4: Thêm vào giỏ (Có kiểm tra tồn kho & biến thể)"""
    product = get_product_by_id(product_id)
    if not product:
        return {"success": False, "message": "Sản phẩm không tồn tại"}

    # Check trạng thái chung
    if product.get('status') == 'out_of_stock':
        return {"success": False, "message": "Sản phẩm đã ngừng kinh doanh"}

    # Check biến thể và tồn kho
    variant_name = ""
    if variant_id and 'variants' in product:
        variant = next((v for v in product['variants'] if v['id'] == variant_id), None)
        if not variant:
            return {"success": False, "message": "Biến thể không hợp lệ"}
        if variant['stock'] < qty:
            return {"success": False, "message": f"Mẫu {variant['name']} đã hết hàng!"}
        variant_name = variant['name']

    for item in MOCK_CART:
        if item['product_id'] == product_id and item.get('variant_id') == variant_id:
            item['qty'] += qty
            return {"success": True, "message": "Đã cập nhật số lượng trong giỏ!"}
    
    MOCK_CART.append({
        'product_id': product_id, 
        'qty': qty, 
        'variant_id': variant_id,
        'variant_name': variant_name
    })
    return {"success": True, "message": "Thêm vào giỏ thành công!"}

def update_cart_qty(product_id, change):
    for item in MOCK_CART:
        if item['product_id'] == product_id:
            item['qty'] += change
            if item['qty'] < 1: item['qty'] = 1
            return

def remove_from_cart(product_id):
    global MOCK_CART
    MOCK_CART = [item for item in MOCK_CART if item['product_id'] != product_id]

def move_to_wishlist(product_id):
    remove_from_cart(product_id)
    if product_id not in MOCK_WISHLIST:
        MOCK_WISHLIST.append(product_id)

def apply_voucher_code(code):
    global APPLIED_VOUCHER
    if code == 'GIAM10':
        APPLIED_VOUCHER = code
        return True
    return False
def clear_cart():
    """Làm sạch giỏ hàng sau khi thanh toán thành công"""
    global MOCK_CART, APPLIED_VOUCHER
    MOCK_CART.clear() 
    APPLIED_VOUCHER = None # Reset voucher