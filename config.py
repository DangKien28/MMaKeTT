import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Giữ nguyên các key bí mật của bạn
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    FB_APP_ID = os.getenv("FB_APP_ID")
    FB_APP_SECRET = os.getenv("FB_APP_SECRET")
    APP_EMAIL= os.getenv("APP_EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    # --- PHẦN SỬA LỖI DATABASE ---
    # Lấy DATABASE_URL từ môi trường của Render
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # Nếu biến DATABASE_URL tồn tại (tức là đang chạy trên Render),
        # hãy sử dụng trực tiếp giá trị đó.
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Nếu không, (chạy local), dùng database MySQL của bạn
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_password@localhost/your_database_name"

    SQLALCHEMY_TRACK_MODIFICATIONS = False