from flask import Flask

from controller.home_controller import home_bp   
from controller.shop_controller import shop_bp   
from controller.cart_controller import cart_bp   
from controller.order_controller import order_bp 
from controller.notification_controller import noti_bp 
from controller.user_client_controller import user_bp

app = Flask(__name__)

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    app.config['SECRET_KEY'] = 'dev_key_123'
    print("⚠️ Cảnh báo: Không tìm thấy file config.py, đang dùng cấu hình mặc định.")

app.register_blueprint(home_bp)

app.register_blueprint(shop_bp)

app.register_blueprint(cart_bp)

app.register_blueprint(order_bp)
app.register_blueprint(noti_bp)

app.register_blueprint(user_bp)

if __name__ == '__main__':
    print("🚀 Server đang chạy tại: http://127.0.0.1:5000/")
    app.run(debug=True)

    