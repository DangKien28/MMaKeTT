from flask import Blueprint, jsonify, render_template, redirect, url_for, request, session, current_app
from model.user import User, find_user_by_email, Account, Gender
from datetime import date
from .oauth_controller import oauth
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth_bp = Blueprint("auth", __name__)

#dang ky
@auth_bp.route("/register", methods = ["GET"])
def register():
  return render_template("register.html")
  
@auth_bp.route('/api/register', methods = ["POST"])
def api_register():
  username = request.form.get("username")
  email = request.form.get("email")
  phone = request.form.get("phone")
  password = request.form.get("password")

  user = User(username, email, phone, password)
  user.save()
  userAccount = Account(date.today(), Gender.OTHER, "default not set", "default not set", date.today(), "default not set", user_id=user.id)
  userAccount.save_account()
  return redirect(url_for("auth.login"))

@auth_bp.route('/api/check_email', methods = ["POST"])
def check_email():
  data = request.get_json()
  email_to_check = data.get("email")
  temp_user = find_user_by_email(email_to_check)

  if temp_user:
    return jsonify({"status_user": True})
  else:
    return jsonify({"status_user": False})

#dang nhap
# @auth_bp.route("/login", methods = ["GET", "POST"])
# def login():
#   if request.method=="POST":
#     eMail = request.form.get("email")
#     password = request.form.get("password")

#     result = find_user_by_email(eMail)

#     if result and result.password==password:
#       print("Tim thay tai khoan------------------------------------")
#       print("Ket qua result sau khi tim: ", result.email, result.password)
#       session["user"] = {
#         "id": result.id,
#         "email": result.email,
#         "name": result.name,
#         "phone": result.phone
#       }
#       print("session: ", result.email, " ", result.name)
#       return redirect(url_for("home.index"))
#     else:
#       print("Sai email or mat khau")
#       return redirect(url_for("auth.login"))
#   return render_template("login.html")
  
@auth_bp.route("/login", methods = ["GET"])
def login():
  return render_template("login.html")

@auth_bp.route("/api/login", methods = ["POST"])
def api_login():
  login_data = request.get_json()
  login_email = login_data["email"]
  login_password = login_data["password"]

  temp_user = find_user_by_email(login_email)
  if (not temp_user):
    return jsonify({"status": "not-register"})
  else:
    if login_password != temp_user.password:
      return jsonify({"error": "incorrect-password"})
    else:
      session["user"] = {
        "id": temp_user.id,
        "email": temp_user.email,
        "name": temp_user.name
      }
      return jsonify(
        {
          "status": "success",
          "redirect_url": url_for("home.index")
        }
      )
  

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
  user = find_user_by_email(user_info["email"])

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

  user = find_user_by_email(placeholder_email)
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


#Gửi email xác thực
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
    return jsonify({"message": "success"}), 200
  else:
    return jsonify({"message": "failed"}), 500
  
@auth_bp.route('/verify-code', methods = ["POST"])
def verify_code():
  data = request.get_json()
  user_code = data.get("code")
  stored_code = session.get('verification_code')
  if not stored_code:
    return jsonify({"message": "required"}), 400

  print(stored_code)
  print(user_code)
  if user_code == stored_code:
    session['is_verified'] = True # Cập nhật trạng thái đã xác thực
    session.pop("verification_code")
    return jsonify({"message": "Verified"}), 200

  else:
    return jsonify({"message": "Un-verify"}), 400
  

