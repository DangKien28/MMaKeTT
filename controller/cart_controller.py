from flask import Blueprint, request, jsonify, render_template
from model.cart import (get_cart_details, add_to_cart, update_cart_qty, 
                        remove_from_cart, move_to_wishlist, apply_voucher_code)

cart_bp = Blueprint('cart', __name__)

# --- ROUTE GIAO DIỆN (Để vào được trang giỏ hàng) ---
@cart_bp.route('/cart')
def cart_page():
    return render_template('cart.html')

# --- API ROUTES ---

@cart_bp.route('/api/cart', methods=['GET'])
def get_cart_api():
    data = get_cart_details()
    return jsonify(data)

@cart_bp.route('/api/cart/add', methods=['POST'])
def add_to_cart_api():
    """EPIC 4: API thêm vào giỏ (Nhận cả biến thể)"""
    data = request.json
    product_id = data.get('product_id')
    qty = int(data.get('qty', 1))
    variant_id = data.get('variant_id') # Lấy ID biến thể
    
    result = add_to_cart(product_id, qty, variant_id)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@cart_bp.route('/api/cart/update', methods=['POST'])
def update_qty_api():
    data = request.json
    update_cart_qty(data.get('product_id'), data.get('change'))
    return jsonify(get_cart_details())

@cart_bp.route('/api/cart/remove', methods=['POST'])
def remove_item_api():
    data = request.json
    remove_from_cart(data.get('product_id'))
    return jsonify(get_cart_details())

@cart_bp.route('/api/cart/wishlist', methods=['POST'])
def to_wishlist_api():
    data = request.json
    move_to_wishlist(data.get('product_id'))
    return jsonify(get_cart_details())

@cart_bp.route('/api/cart/voucher', methods=['POST'])
def apply_voucher_api():
    code = request.json.get('code')
    success = apply_voucher_code(code)
    msg = "Áp dụng mã GIAM10 thành công!" if success else "Mã giảm giá không hợp lệ."
    return jsonify({"message": msg, "data": get_cart_details()})