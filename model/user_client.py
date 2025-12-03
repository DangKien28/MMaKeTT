# model/user_client.py
MOCK_USER = {
    "id": "U001",
    "name": "Nguyễn Văn Khách",
    "email": "khachhang@example.com",
    "phone": "0909123456",
    "address": "TP. Hồ Chí Minh",
    "avatar": "https://cdn-icons-png.flaticon.com/512/149/149071.png"
}

def get_current_user():
    """Lấy thông tin user hiện tại"""
    return MOCK_USER

def update_user_profile(data):
    """Cập nhật thông tin và link ảnh"""
    global MOCK_USER
    
    if data.get('name'): MOCK_USER['name'] = data['name']
    if data.get('phone'): MOCK_USER['phone'] = data['phone']
    if data.get('address'): MOCK_USER['address'] = data['address']
    if data.get('avatar'): MOCK_USER['avatar'] = data['avatar']
    
    return MOCK_USER