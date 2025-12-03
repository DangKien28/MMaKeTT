# model/shop.py

MOCK_SHOPS = []

def create_shop(data):
    """Tạo mới yêu cầu mở gian hàng (MMK-44, MMK-52)"""
    new_shop = {
        "id": len(MOCK_SHOPS) + 1,
        "owner_name": data.get('owner_name'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "shop_name": data.get('shop_name', 'Chưa đặt tên'),
        "address": "",
        "avatar": "", 
        "banner": "", 
        "policy": "", 
        "business_license": data.get('business_license'), 
        "status": "pending", 
        "is_auto_approved": False
    }
    
    if "VIP" in new_shop['owner_name'].upper():
        new_shop['status'] = 'active'
        new_shop['is_auto_approved'] = True
        
    MOCK_SHOPS.append(new_shop)
    return new_shop

def update_shop_info(shop_id, data):
    """Cập nhật thông tin gian hàng (MMK-51, MMK-57, MMK-56)"""
    for shop in MOCK_SHOPS:
        if str(shop['id']) == str(shop_id):
            shop['shop_name'] = data.get('shop_name', shop['shop_name'])
            shop['address'] = data.get('address', shop['address'])
            shop['policy'] = data.get('policy', shop['policy'])
            if data.get('avatar'): shop['avatar'] = data['avatar']
            if data.get('banner'): shop['banner'] = data['banner']
            return shop
    return None

def get_all_shops():
    return MOCK_SHOPS

def approve_shop_status(shop_id, status):
    """Duyệt hoặc từ chối shop (MMK-61, MMK-59)"""
    for shop in MOCK_SHOPS:
        if str(shop['id']) == str(shop_id):
            shop['status'] = status
            return shop
    return None