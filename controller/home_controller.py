from flask import Blueprint, render_template, session, jsonify, request
from model.product import Product, all_products
from model.user import find_by_id, update_account, update_account_info, find_user_by_id
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

home_bp = Blueprint("home", __name__)

#lay user hien tai
def get_current_user():
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            return find_user_by_id(user_id)
    except:
        return None
    return None

@home_bp.route("/")
def index():
  user = get_current_user()
  user_info = None
  if user:
      user_info = {
          "name": user.name,
          "email": user.email,
      }
  products = all_products()
  return render_template("index.html", user_info=user_info, products=products)

@home_bp.route("/api/products")
def api_products():
  products = all_products()
  product_list = []
  for p in products:
    product_list.append({
      "name": p.name,
      "price": p.price,
      "rating": p.rating,
      "image_url": p.image_url
    })
  return jsonify(product_list)

# @home_bp.route("/account")
# def account_info():
#   return render_template("account_1.html")

# @home_bp.route("/api/account")
# def account():
#   user_info = session["user"]
#   account_detail = find_by_id(user_info["id"])

#   user_data_json = {
#     "username": user_info["name"],
#     "email": user_info["email"],
#     "phone": user_info["phone"],
#     "birth": account_detail.birth,
#     "gender": account_detail.gender.value,
#     "address": account_detail.address,
#     "id_card": account_detail.id_card,
#     "date_of_issue": account_detail.date_of_issue,
#     "place_of_issue": account_detail.place_of_issue
#   }
#   return jsonify(user_data_json)

# @home_bp.route("/api/account/update", methods = ["POST"])
# def update_user_account():
#   user_id = session["user"]["id"]
#   data = request.get_json()

#   #Bảng users
#   user_login = update_account( user_id, data['username'], data['email'], data['phone'])
#   user_detail = update_account_info(user_id, data)

#   if user_login and user_detail:
#     session["user"]["name"] = data["username"]
#     session["user"]["phone"] = data["phone"]
#     session["user"]["email"] = data["email"]
#     session.modified=True
#     return jsonify({
#       "status": "success",
#       "message": "Cập nhật thành công"
#       })
#   else:
#     return jsonify({
#       "status": "error",
#       "message": "Cập nhật thất bại"
#       }), 500


# New account updated

@home_bp.route('/account')
@jwt_required()
def account_page():
    """
    Render trang chính với sidebar và một khu vực nội dung trống.
    """
    return render_template('account_1.html')
    # return render_template('gmy_account_2.html')

# route (partials)
@home_bp.route('/account/information')
def get_information():
    return render_template('partials/_information.html')

@home_bp.route('/account/bank')
def get_bank():
    return render_template('partials/_bank.html')

@home_bp.route('/account/change-password')
def get_change_password():
    return render_template('partials/_change_password.html')

@home_bp.route('/account/privacy-settings')
def get_privacy_settings():
    return render_template('partials/_privacy_settings.html')

@home_bp.route('/account/purchase-order')
def get_purchase_order():
    return render_template('partials/_purchase_order.html')

@home_bp.route('/account/update-order')
def get_update_order():
    return render_template('partials/_update_order.html')

@home_bp.route('/account/promotion')
def get_promotion():
    return render_template('partials/_promotion.html')

# Route cho voucher (ví dụ)
@home_bp.route('/account/voucher')
def get_voucher():
    return "<h3>My Vouchers</h3><p class='empty-message'>You don't have any vouchers yet.</p>"

@home_bp.route("/api/basicInfo", methods=["GET"])
@jwt_required()
def basic_information():
    current_user_id = get_jwt_identity()
    user_detail = find_by_id(current_user_id)
    user_core = find_user_by_id(current_user_id)
    
    return jsonify(
        {
            "username": user_core.name,
            "email": user_core.email,
            "phone": user_core.phone,
            "date_of_birth": user_detail.birth,
            "gender": user_detail.gender.value,
            "address": user_detail.address,
            "id_card": user_detail.id_card,
            "date_of_issue": user_detail.date_of_issue,
            "place_of_issue": user_detail.place_of_issue
        }
    )

@home_bp.route("/api/update_account", methods = ["POST"])
@jwt_required()
def update_information():
    user_info = request.get_json()
    user_id = get_jwt_identity()

    print(user_info)
    print(user_id)

    account = update_account(user_id, user_info["username"], user_info["email"], user_info["phone"])
    account_info = update_account_info(user_id, user_info)    

    if account and account_info:
        return jsonify(
            {
                "status": "success",
                "message": "Cập nhật thành công"
            }
        )
    else:
        return jsonify(
            {
                "status": "failed",
                "message": "Cập nhật thất bại!!!"
            }
        )