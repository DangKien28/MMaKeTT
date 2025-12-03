import datetime
import random
from model.cart import get_cart_details, clear_cart
from model.notification import add_notification, add_seller_notification

MOCK_ORDERS = []

def create_new_order(customer_data):
    cart_info = get_cart_details()
    if not cart_info['items']: return {"success": False, "message": "Giỏ hàng trống!"}

    order_id = f"ORD-{random.randint(10000, 99999)}"
    
    new_order = {
        "id": order_id,
        "customer": {
            "name": customer_data.get('name'),
            "phone": customer_data.get('phone'),
            "address": customer_data.get('address'),
        },
        "items": cart_info['items'],
        "financials": {
            "subtotal": cart_info['subtotal'],
            "shipping_fee": cart_info['shipping_fee'],
            "discount": cart_info['discount'],
            "total": cart_info['final_total']
        },
        "payment_method": customer_data.get('payment_method'),
        # Các trạng thái: pending, confirmed, shipping, delivered, cancelled
        "status": "pending", 
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "history": [ 
            {"status": "pending", "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ]
    }

    if new_order['payment_method'] == 'banking':
        new_order['history'].append({"status": "paid", "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    MOCK_ORDERS.append(new_order)
    clear_cart()

    add_notification("📦 Đặt hàng thành công!", f"Đơn hàng {order_id} đang chờ xác nhận.", "order")
    add_seller_notification("💰 Có đơn hàng mới!", f"Đơn {order_id} từ {new_order['customer']['name']}", "order")

    return {"success": True, "message": "Đặt hàng thành công!", "order_id": order_id}

def get_order_by_id(order_id):
    for order in MOCK_ORDERS:
        if order['id'] == order_id:
            return order
    return None

def get_my_orders():
    """MMK-179: Lấy danh sách đơn hàng (Mới nhất lên đầu)"""
    return sorted(MOCK_ORDERS, key=lambda x: x['created_at'], reverse=True)

def update_order_status(order_id, new_status):
    """MMK-182: Cập nhật trạng thái và gửi thông báo"""
    order = get_order_by_id(order_id)
    if not order: return False

    order['status'] = new_status
    order['history'].append({
        "status": new_status,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    msg_map = {
        "confirmed": "Đơn hàng đã được xác nhận và đang đóng gói.",
        "shipping": "Đơn hàng đang được giao đến bạn.",
        "delivered": "Giao hàng thành công. Hãy đánh giá nhé!",
        "cancelled": "Đơn hàng đã bị hủy."
    }
    
    if new_status in msg_map:
        add_notification(
            title=f"Cập nhật đơn {order_id}",
            message=msg_map[new_status],
            noti_type="order"
        )
    
    return True