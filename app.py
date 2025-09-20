from flask import Flask
from controller import auth_controller, home_controller
from config import Config
from controller.oauth_controller import init_oauth

app = Flask(__name__)
app.config.from_object(Config)

init_oauth(app)
# auth_controller.google = google
# auth_controller.facebook = facebook



app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(home_controller.home_bp)

if __name__=="__main__":
  app.run(debug=True)