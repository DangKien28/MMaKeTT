from flask import Blueprint, render_template, session, redirect, url_for
from utils.session import is_logged_in

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
  if is_logged_in():
    print("Da co trong session")
    return render_template("index.html", username = session["username"])
  else:
    print("Can dang nhap truoc")
    return render_template("index.html")