from flask import Blueprint, render_template, redirect, url_for, request, session
from model.user import User

auth_bp = Blueprint("auth", __name__)

google = None

#dang ky
@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
  if request.method=="POST":
    eMail = request.form.get("email")
    name = request.form.get("username")
    phone = request.form.get("phone")
    password = request.form.get("password")

    if not eMail or not name or not phone or not password:
      print("Nhap day du thong tin moi duoc dang ky")
      return render_template("register.html")
    user = User(name, eMail, phone, password)

    if user.check_account():
      print("Email da duoc dang ky")
      return render_template("register.html")
    user.save()
    return redirect(url_for("auth.login"))
  return render_template("register.html")
  
#dang nhap
@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
  if request.method=="POST":
    eMail = request.form.get("email")
    name = request.form.get("username")
    phone = request.form.get("phone")
    password = request.form.get("password")

    user = User(name, eMail, phone, password)
    result = user.find_user()
    print("Ket qua result sau khi tim: ", result.email, result.password)

    if result:
      print("Tim thay tai khoan------------------------------------")
      session["user"] = {
        "email": result.email,
        "name": result.name
      }
      print("session: ", result.email, " ", result.name)
      return redirect(url_for("home.index"))
    else:
      print("Sai email or mat khau")
      return redirect(url_for("auth.login"))
  return render_template("login.html")
  

#dang xuat
@auth_bp.route("/logout")
def logout():
  session.clear()
  print("Da dang xuat")
  return redirect(url_for("home.index"))

#SOCIAL
#DANG NHAP BANG GOOGLE

@auth_bp.route("/login/google")
def google_login():
  redirect_uri = url_for("auth.authorize_google", _external=True)
  print("direct:")
  print(redirect_uri)
  return google.authorize_redirect(redirect_uri)

@auth_bp.route("/callback/google")
def authorize_google():
  token = google.authorize_access_token()
  resp = google.get("userinfo")
  user_info = resp.json()
  session["user"] = user_info
  return redirect(url_for("home.index"))