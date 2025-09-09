from flask import Flask
from controller import auth_controller, home_controller

app = Flask(__name__)
app.secret_key = "tk_message"
app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(home_controller.home_bp)

if __name__=="__main__":
  app.run(debug=True)