from flask import Blueprint, jsonify, render_template, redirect, url_for, request, session, current_app
from model.user import User, find_user, Account, Gender
from datetime import date
from .oauth_controller import oauth
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth_bp = Blueprint("auth", __name__)

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

    session.pop('verification_code', None)
    session.pop('verification_email', None)
    session.pop('is_verified', None)

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

#SOCIAL---------------------------------------------------------
#DANG NHAP BANG GOOGLE

@auth_bp.route("/login/google")
def google_login():
  redirect_uri = url_for("auth.authorize_google", _external=True)
  print("direct:")
  print(redirect_uri)
  return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route("/callback/google")
def authorize_google():
  token = oauth.google.authorize_access_token()
  resp = oauth.google.get("userinfo")
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
    user = new_user

  if user:
    session["user"] = {
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "phone": "GG Phone not set"
    }
    return redirect(url_for("home.index"))
  return redirect(url_for("auth.login"))

#DANG NHAP BANG FACEBOOK
@auth_bp.route("/login/facebook")
def facebook_login():
  redirect_uri = url_for("auth.authorize_facebook", _external=True)
  return oauth.facebook.authorize_redirect(redirect_uri)

@auth_bp.route("/callback/facebook")
def authorize_facebook():
  token = oauth.facebook.authorize_access_token()
  resp = oauth.facebook.get('me?fields=id,name,picture')
  user_info_fb = resp.json()

  user_info = {
    "name": user_info_fb.get("name"),
    "id": user_info_fb.get("id"),
    "picture": user_info_fb.get("picture", {}).get("data", {}).get("url")
  }

  print(user_info["name"], " ", user_info["id"])
  placeholder_email = f"{user_info["name"]}@example.com"

  user = find_user(placeholder_email)
  if not user:
    new_user = User(
      name=user_info["name"],
      email=placeholder_email,
      phone="not set",
      password="default_password"
    )
    new_user.save()
    user_account = Account(date.today(), Gender.OTHER, "Address FB not set", "ID Card FB not set", date.today(), "Place not set", user_id=new_user.id)
    user_account.save_account()
    user = new_user

  if user:
    session["user"] = {
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "phone": "FB Phone not set"
    }
    return redirect(url_for("home.index"))
  
def send_verification_email(recipient_email, code):
  sender_email = current_app.config.get("APP_EMAIL")
  sender_password = current_app.config.get("APP_PASSWORD")

  if not sender_email or not sender_password:
    print("Lỗi khi load APP_EMAIL và APP_PASSWORD")
    return False
  message = MIMEMultipart("alternative")
  message["Subject"] = f"Mã xác thực MMaKeTT của bạn là {code}"
  message["From"] = f"MMaKeTT <{sender_email}>"
  message["To"] = recipient_email

  html = f"""
          <body>
            <div style="font-family: Arial, sans-serif; text-align: center; color: #333;">
              <h2>Xác thực tài khoản MMaKeTT</h2>
              <p>Cảm ơn bạn đã đăng ký. Mã xác thực của bạn là:</p>
              <p style="font-size: 24px; font-weight: bold; color: #007bff;">{code}</p>
              <p>Vui lòng nhập mã này vào trang đăng ký để hoàn tất.</p>
              <p style="font-size: 0.9em; color: #777;">Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email này.</p>
            </div>
          </body>
        </html>
          """
  message.attach(MIMEText(html, "html"))

  #Gửi email
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())

  print(f"Đã gửi email xác thực tới {recipient_email}")
  return True

#API mã xác thực
@auth_bp.route("/send-verification-code", methods = ["POST"])
def send_code():
  data = request.get_json()
  email = data.get("email")

  code = f"{random.randint(0, 999999):06d}"

  session['verification_code'] = code
  session['verification_email'] = email
  session['is_verified'] = False

  if send_verification_email(email, code):
    return jsonify({"message": "Mã xác thực đã được gửi tới email của bạn."}), 200
  else:
    return jsonify({"message": "Không thể gửi mã. Vui lòng thử lại sau."}), 500
  
@auth_bp.route('/verify-code', methods = ["POST"])
def verify_code():
  data = request.get_json()
  user_code = data.get("code")
  stored_code = session.get('verification_code')
  if not stored_code:
    return jsonify({"message": "Vui lòng yêu cầu gửi mã trước."}), 400

  if user_code == stored_code:
    session['is_verified'] = True # Cập nhật trạng thái đã xác thực
    return jsonify({"message": "Xác thực thành công!"}), 200
  else:
    return jsonify({"message": "Mã xác thực không đúng."}), 400