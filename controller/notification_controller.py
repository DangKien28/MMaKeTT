from flask import Blueprint, jsonify, request
from model.notification import (get_notifications, count_unread, mark_read_all,
                                get_seller_notifications, count_seller_unread, mark_seller_read_all, add_seller_notification)

noti_bp = Blueprint('notification', __name__)

@noti_bp.route('/api/notifications', methods=['GET'])
def get_noti_api():
    data = get_notifications()
    unread = count_unread()
    return jsonify({"notifications": data, "unread_count": unread})

@noti_bp.route('/api/notifications/read', methods=['POST'])
def mark_read_api():
    mark_read_all()
    return jsonify({"success": True})

@noti_bp.route('/api/seller/notifications', methods=['GET'])
def get_seller_noti_api():
    """MMK-142: Lấy thông báo cho người bán"""
    data = get_seller_notifications()
    unread = count_seller_unread()
    return jsonify({"notifications": data, "unread_count": unread})

@noti_bp.route('/api/seller/notifications/read', methods=['POST'])
def mark_seller_read_api():
    mark_seller_read_all()
    return jsonify({"success": True})

@noti_bp.route('/api/seller/test-noti', methods=['POST'])
def test_seller_noti_api():
    """Giả lập sự kiện khách nhắn tin hoặc hủy đơn (MMK-138, 139)"""
    data = request.json
    noti_type = data.get('type') 
    
    if noti_type == 'chat':
        add_seller_notification("💬 Tin nhắn mới", "Khách hàng Nguyễn Văn A: 'Shop ơi còn hàng không?'", "chat")
    elif noti_type == 'cancel':
        add_seller_notification("⚠️ Yêu cầu hủy đơn", "Khách muốn hủy đơn ORD-12345. Lý do: Đổi ý.", "cancel")
        
    return jsonify({"success": True, "message": "Đã gửi thông báo giả lập!"})