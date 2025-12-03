# model/product.py

MOCK_PRODUCTS = [
    {
        "id": "SP001", 
        "name": "Áo Anh 7", 
        "vendor": "CR7", 
        "price": 1500000, 
        "category": "Áo", 
        "views": 850, 
        "release_date": "2024-05-10",
        "status": "in_stock", 
        
        "description": "Áo anh 7 mang vào đá như anh Si Tạ",
        "attributes": [ 
            {"name": "Kiểu", "value": "Áo rời"},
            {"name": "Cách", "value": "Mặc vào"},
            {"name": "Trọng lượng", "value": "500g"}
        ],
        "images": [ 
            "https://sumstore.vn/wp-content/uploads/2024/04/cr7-fix.jpg",
            "https://sumstore.vn/wp-content/uploads/2024/04/cr7-fix.jpg",
            "https://sumstore.vn/wp-content/uploads/2024/04/cr7-fix.jpg"
        ],
        "video": "https://www.youtube.com/embed/4H9F9H-Jc6c", 
        
        "shop": { 
            "id": "S01",
            "name": "Messi",
            "avatar": "https://media-cdn-v2.laodong.vn/storage/newsportal/2025/11/17/1610695/Messi-4.jpeg",
            "rating": 4.9
        },

        "reviews": [ 
            {"user": "Jack", "rating": 5, "comment": "Mặc sướng vl thề", "date": "2024-11-01"},
            {"user": "Viruss", "rating": 4, "comment": "Những người thích anh, anh cản đc", "date": "2024-10-20"}
        ],
        "rating_avg": 4.5, 

        "variants": [
            {"id": "v1", "name": "Đen - Red Switch", "stock": 10},
            {"id": "v2", "name": "Trắng - Blue Switch", "stock": 0}, 
        ]
    },
    {
        "id": "SP002", 
        "name": "Áo Anh Si", 
        "vendor": "Anh Si 10", 
        "price": 800000, 
        "category": "Áo", 
        "views": 1200, 
        "release_date": "2024-06-01",
        "status": "in_stock",
        "description": "Áo đá bóng nha mấy bé",
        "images": ["https://media-cdn-v2.laodong.vn/storage/newsportal/2025/11/17/1610695/Messi-4.jpeg"], 
        "video": "",
        "shop": {"id": "S02", "name": "Si Tạ VN", "avatar": "https://media-cdn-v2.laodong.vn/storage/newsportal/2025/11/17/1610695/Messi-4.jpeg", "rating": 4.8},
        "reviews": [],
        "rating_avg": 5.0,
        "variants": [
            {"id": "v3", "name": "Đen", "stock": 50},
            {"id": "v4", "name": "Hồng", "stock": 5}
        ]
    },
]

def get_all_products():
    return MOCK_PRODUCTS

def get_product_by_id(pid):
    for p in MOCK_PRODUCTS:
        if p['id'] == pid:
            return p
    return None