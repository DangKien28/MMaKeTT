from flask import Flask
from controller import auth_controller, home_controller, cart_controller
from config import Config
from controller.oauth_controller import init_oauth
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

init_oauth(app)
# auth_controller.google = google
# auth_controller.facebook = facebook



app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(home_controller.home_bp)
app.register_blueprint(cart_controller.cart_bp)


if __name__=="__main__":
  app.run(debug=True)