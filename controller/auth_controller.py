from flask import Blueprint, render_template, redirect, url_for, request
from model.user import User
from utils.session import login_user, logout_user

auth_bp = Blueprint("auth", __name__)

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
      login_user(result)
      print("session: ", result.email, " ", result.name)
      return redirect(url_for("home.index"))
    else:
      print("Sai email or mat khau")
      return redirect(url_for("auth.login"))
  return render_template("login.html")
  
@auth_bp.route("/logout")
def logout():
  logout_user()
  print("Da dang xuat")
  return redirect(url_for("home.index"))