from flask import Blueprint, jsonify, render_template, redirect, url_for, request, session, current_app
from model.user import User, find_user_by_email, Account, Gender, update_password_by_id
from datetime import date
from .oauth_controller import oauth
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From
import random
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt_identity

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
      access_token = create_access_token(identity=str(temp_user.id))
      resp = jsonify({
        "status": "success",
        "redirect_url": url_for("home.index")
      })
      set_access_cookies(resp, access_token)
      return resp

#dang xuat
@auth_bp.route("/logout")
def logout():
  resp = redirect(url_for("home.index"))
  unset_jwt_cookies(resp)
  print("Da dang xuat")
  return resp

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
    access_token = create_access_token(identity=str(user.id))
    response = redirect(url_for("home.index"))
    set_access_cookies(response, access_token)
    return response
  
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
    access_token = create_access_token(str(user.id))
    response = redirect(url_for("home.index"))
    set_access_cookies(response, access_token)
    return response
  return redirect(url_for("auth.login"))


def send_verification_email(recipient_email, code):
  sender_email = current_app.config.get("SENDGRID_MAIL")
  api_key = current_app.config.get("SENDGRID_KEY")

  if not sender_email or not api_key:
    print("Lỗi khi không tìm thấy SENDGRID_MAIL hoặc SENDGRID_KEY")
    return False
  
  html_content = f"""
    <html>
      <body>
        <div style="font-family: Arial, sans-serif; text-align: center; color: #333;">
          <h2>Xác thực tài khoản MMaKeTT</h2>
          <p>Cảm ơn bạn đã đăng ký. Mã xác thực của bạn là:</p>
          <p style="font-size: 24px; font-weight: bold; color: #007bff;">{code}</p>
        </div>
      </body>
    </html>
  """

  message = Mail(
    from_email=From(sender_email, 'MMaKeTT'),
    to_emails=recipient_email,
    subject=f"Mã xác thực MMaKeTT của bạn là {code}",
    html_content=html_content
  )

  try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)

    print(f"Email đã gửi")
    return response.status_code == 202
  except Exception as e:
    print(f"Lỗi khi gửi email qua Sendgrid {e}")
    return False
  
@auth_bp.route("/send-verification-code", methods=["POST"])
def send_email():
  data = request.get_json()
  email = data.get("email")

  if not email:
    return jsonify(
      {
        "message": "Email là bắt buộc"
      }
    ), 400
  
  code = f"{random.randint(0, 999999):06d}"

  session['verification_code'] = code
  session['verification_email'] = email
  session['is_verified'] = False

  if send_verification_email(email, code):
    return jsonify({"message": "Send success"}), 200
  else:
    session.pop('verification_code', None)
    session.pop('verification_email', None)
    return jsonify({"message":"Send failed"}), 500

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
  
@auth_bp.route("/api/change-password", methods=["POST"])
@jwt_required()
def change_password():
  id = get_jwt_identity()
  data = request.get_json()
  code = data.get("code")
  new_password = data.get("new_password")

  stored_code = session.get("verification_code")

  if not stored_code or code!=stored_code:
    return jsonify(
      {
        "status": "error",
        "message": "Mã xác thực không đúng hoặc đã hết hạn"
      }
    )
  
  try:
    update_password_by_id(id, new_password)

    session.pop("verification_code", None)
    session.pop("verification_email", None)
    session.pop("is_verified", None)

    resp = jsonify(
      {
        "status": "success",
        "message": "Đổi mật khẩu thành công. Đăng nhập lại!"
      }
    )
    unset_jwt_cookies(resp)
    return resp, 200
  except Exception as e:
    print(f"Lỗi đổi mật khẩu: {e}")
    return jsonify(
      {
        "status": "error",
        "message": "Lỗi hệ thống"
      }
    ), 500
  