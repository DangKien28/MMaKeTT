from flask import Blueprint, render_template, redirect, url_for, request, session
from model.user import User, find_user, Account, Gender
from datetime import date

auth_bp = Blueprint("auth", __name__)

google = None
facebook = None

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
    
    user_account = Account(date.today(), Gender.OTHER, "Address not set", "ID Card not set", date.today(), "Place not set", user_id=user.id)
    user_account.save_account()

    return redirect(url_for("auth.login"))
  return render_template("register.html")
  
#dang nhap
@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
  if request.method=="POST":
    eMail = request.form.get("email")
    password = request.form.get("password")

    result = find_user(eMail)
    

    if result and result.password==password:
      print("Tim thay tai khoan------------------------------------")
      print("Ket qua result sau khi tim: ", result.email, result.password)
      session["user"] = {
        "id": result.id,
        "email": result.email,
        "name": result.name,
        "phone": result.phone
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

  user = find_user(user_info["email"])

  if not user:
    new_user = User(
      name=user_info.get("name"),
      email=user_info.get("email"),
      phone="not set",
      password="default_password"
    )
    new_user.save()
    user_account = Account(date.today(), Gender.OTHER, "Address GG not set", "ID Card GG not set", date.today(), "Place not set", user_id=new_user.id)
    user_account.save_account()
    user = find_user(user_info["email"])

  if user:
    session["user"] = {
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "phone": "GG Phone not set"
    }
    return redirect(url_for("home.index"))

#DANG NHAP BANG FACEBOOK
@auth_bp.route("/login/facebook")
def facebook_login():
  redirect_uri = url_for("auth.authorize_facebook", _external=True)
  return facebook.authorize_redirect(redirect_uri)

@auth_bp.route("/callback/facebook")
def authorize_facebook():
  token = facebook.authorize_access_token()
  resp = facebook.get('me?fields=id,name,picture')
  user_info_fb = resp.json()

  user_info = {
    "name": user_info_fb.get("name"),
    "id": user_info_fb.get("id"),
    "picture": user_info_fb.get("picture", {}).get("data", {}).get("url")
  }

  print(user_info["name"], " ", user_info["id"])
  placeholder_email = f"{user_info["id"]}@facebook.placeholder.com"

  user = find_user(placeholder_email)
  if not user:
    new_user = User(
      name=user_info["name"],
      email=placeholder_email,
      phone="not set",
      password="default_password"
    )
    new_user.save()
    user = find_user(placeholder_email)
  if user:
    session["user"] = {
      "id": user.id,
      "name": user.name,
      "email": user.email
    }
  return redirect(url_for("home.index"))