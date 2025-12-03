# controller/order_controller.py
from flask import Blueprint, render_template, request, jsonify
from model.order import create_new_order, get_order_by_id, get_my_orders, update_order_status

order_bp = Blueprint('order', __name__)

# --- VIEW ROUTES ---
@order_bp.route('/checkout')
def checkout_page():
    return render_template('checkout.html')

@order_bp.route('/order-success/<order_id>')
def order_success_page(order_id):
    return render_template('order_success.html', order_id=order_id)

# --- EPIC 10: ROUTES MỚI ---
@order_bp.route('/my-orders')
def order_history_page():
    """MMK-179: Trang danh sách đơn hàng"""
    return render_template('order_history.html')

@order_bp.route('/order-tracking/<order_id>')
def order_tracking_page(order_id):
    """MMK-178: Trang chi tiết theo dõi đơn hàng"""
    return render_template('order_detail.html', order_id=order_id)

# --- API ROUTES ---
@order_bp.route('/api/order/create', methods=['POST'])
def create_order_api():
    data = request.json
    if not data.get('name') or not data.get('phone') or not data.get('address'):
        return jsonify({"success": False, "message": "Thiếu thông tin!"}), 400
    
    result = create_new_order(data)
    if result['success']: return jsonify(result)
    else: return jsonify(result), 400

@order_bp.route('/api/order/<order_id>', methods=['GET'])
def get_order_detail_api(order_id):
    order = get_order_by_id(order_id)
    if order: return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@order_bp.route('/api/my-orders', methods=['GET'])
def get_my_orders_api():
    """Lấy danh sách đơn hàng"""
    return jsonify(get_my_orders())

@order_bp.route('/api/order/update-status', methods=['POST'])
def update_status_api():
    """Giả lập Admin/System cập nhật trạng thái (để test)"""
    data = request.json
    success = update_order_status(data.get('order_id'), data.get('status'))
    return jsonify({"success": success})