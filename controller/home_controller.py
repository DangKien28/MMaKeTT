from flask import Blueprint, render_template, session, jsonify, request
from model.product import Product, all_products
from model.user import find_by_id, update_account, update_account_info
from datetime import datetime

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
  user = session.get("user")
  products = all_products()
  return render_template("index.html", user_info=user, products=products)

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

@home_bp.route("/account")
def account_info():
  return render_template("account.html")

@home_bp.route("/api/account")
def account():
  user_info = session["user"]
  account_detail = find_by_id(user_info["id"])

  user_data_json = {
    "username": user_info["name"],
    "email": user_info["email"],
    "phone": user_info["phone"],
    "birth": account_detail.birth,
    "gender": account_detail.gender.value,
    "address": account_detail.address,
    "id_card": account_detail.id_card,
    "date_of_issue": account_detail.date_of_issue,
    "place_of_issue": account_detail.place_of_issue
  }
  return jsonify(user_data_json)

@home_bp.route("/api/account/update", methods = ["POST"])
def update_user_account():
  user_id = session["user"]["id"]
  data = request.get_json()

  #Bảng users
  user_login = update_account( user_id, data['username'], data['email'], data['phone'])
  user_detail = update_account_info(user_id, data)

  if user_login and user_detail:
    session["user"]["name"] = data["username"]
    session["user"]["phone"] = data["phone"]
    session["user"]["email"] = data["email"]
    session.modified=True
    return jsonify({
      "status": "success",
      "message": "Cập nhật thành công"
      })
  else:
    return jsonify({
      "status": "error",
      "message": "Cập nhật thất bại"
      }), 500
