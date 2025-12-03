# controller/shop_controller.py

from flask import Blueprint, render_template, request, jsonify
from model.shop import create_shop, get_all_shops, update_shop_info, approve_shop_status

shop_bp = Blueprint('shop', __name__)

# --- VIEW ROUTES ---
@shop_bp.route('/seller')
def seller_page():
    return render_template('seller.html')

@shop_bp.route('/admin')
@shop_bp.route('/admin/') 
def admin_page():
    return render_template('admin.html')

# --- API ROUTES ---

@shop_bp.route('/api/shop/register', methods=['POST'])
def register_shop_api():
    data = request.json
    if not data:
        return jsonify({"message": "Dữ liệu không hợp lệ"}), 400
        
    new_shop = create_shop(data)
    msg = "Đăng ký thành công! Vui lòng chờ duyệt."
    if new_shop['is_auto_approved']:
        msg = "Đăng ký thành công! Hệ thống đã tự động duyệt."
        
    return jsonify({"message": msg, "shop": new_shop})

@shop_bp.route('/api/shop/update', methods=['POST'])
def update_shop_api():
    data = request.json
    shop_id = data.get('id')
    updated_shop = update_shop_info(shop_id, data)
    
    if updated_shop:
        return jsonify({"message": "Cập nhật hồ sơ thành công!", "shop": updated_shop})
    return jsonify({"message": "Không tìm thấy Shop"}), 404

@shop_bp.route('/api/admin/shops', methods=['GET'])
def get_all_shops_api():
    return jsonify(get_all_shops())

@shop_bp.route('/api/admin/approve', methods=['POST'])
def approve_shop_api():
    try:
        data = request.json
        shop_id = data.get('id')
        action = data.get('action') 
        
        print(f"DEBUG: Đang xử lý Shop ID: {shop_id}, Action: {action}")

        status = 'active' if action == 'approve' else 'rejected'
        shop = approve_shop_status(shop_id, status)
        
        if not shop:
            return jsonify({"message": f"Lỗi: Không tìm thấy Shop có ID {shop_id}"}), 404

        email = shop.get('email', 'Không có email') 
        notification = f"Đã gửi email thông báo {status} đến {email}"
        
        return jsonify({"message": f"Đã {action} thành công. {notification}", "shop": shop})
        
    except Exception as e:
        print(f"SERVER ERROR: {e}")
        return jsonify({"message": f"Lỗi Server: {str(e)}"}), 500