from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from model.product import Product, all_products 

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
