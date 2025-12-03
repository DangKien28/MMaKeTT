# model/notification.py
import datetime

# --- KHÁCH HÀNG (USER) ---
MOCK_NOTIFICATIONS = [
    {
        "id": 1,
        "title": "🎉 Chào mừng bạn mới!",
        "message": "Tặng bạn mã GIAM10 giảm 10% cho đơn đầu tiên.",
        "type": "promo",
        "date": "2024-11-20 08:00",
        "is_read": False
    }
]

MOCK_SELLER_NOTIFICATIONS = []

def get_notifications():
    return sorted(MOCK_NOTIFICATIONS, key=lambda x: x['id'], reverse=True)

def add_notification(title, message, noti_type="system"):
    new_id = len(MOCK_NOTIFICATIONS) + 1
    new_noti = {
        "id": new_id,
        "title": title,
        "message": message,
        "type": noti_type,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "is_read": False
    }
    MOCK_NOTIFICATIONS.append(new_noti)
    return new_noti

def count_unread():
    return len([n for n in MOCK_NOTIFICATIONS if not n['is_read']])

def mark_read_all():
    for n in MOCK_NOTIFICATIONS:
        n['is_read'] = True

def get_seller_notifications():
    """Lấy danh sách thông báo cho người bán"""
    return sorted(MOCK_SELLER_NOTIFICATIONS, key=lambda x: x['id'], reverse=True)

def add_seller_notification(title, message, noti_type="order"):
    """MMK-141, 145: Tạo thông báo mới cho người bán"""
    new_id = len(MOCK_SELLER_NOTIFICATIONS) + 1
    new_noti = {
        "id": new_id,
        "title": title,
        "message": message,
        "type": noti_type, # order, cancel, chat
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "is_read": False
    }
    MOCK_SELLER_NOTIFICATIONS.append(new_noti)
    return new_noti

def count_seller_unread():
    return len([n for n in MOCK_SELLER_NOTIFICATIONS if not n['is_read']])

def mark_seller_read_all():
    for n in MOCK_SELLER_NOTIFICATIONS:
        n['is_read'] = True