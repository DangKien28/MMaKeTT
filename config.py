import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")

  #GOOGLE
  GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
  GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

  #FACEBOOK
  FB_APP_ID = os.getenv("FB_APP_ID")
  FB_APP_SECRET = os.getenv("FB_APP_SECRET")

      # 2. THÊM PHẦN CẤU HÌNH DATABASE MỚI VÀO ĐÂY
    # Lấy chuỗi kết nối DATABASE_URL từ môi trường của Render
  DATABASE_URL = os.getenv('DATABASE_URL')

  if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
      # Nếu đang chạy trên Render, dùng database Postgres
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql://", 1)
  else:
    # Nếu không, (chạy local), dùng database MySQL của bạn
    # !!! LƯU Ý: Hãy thay đổi thông tin bên dưới cho đúng với máy của bạn !!!
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Dtk.281005@localhost/userdb"

  # Cài đặt bắt buộc cho SQLAlchemy
  SQLALCHEMY_TRACK_MODIFICATIONS = False