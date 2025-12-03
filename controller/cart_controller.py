from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.cart import Cart

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart")
@jwt_required() # phải đăng nhập mới vào được trang giỏ hàng
def view_cart():
    return render_template("cart.html")

@cart_bp.route("/api/cart/items", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()

    own_cart = Cart(user_id)
    own_cart.load_from_db()

    result = []
    for item in own_cart.cartList:
        result.append({
            "product_id": item.product_id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity,
            "image_url": item.image_url,
            "total": item.total_price()
        })
    return jsonify(result)

@cart_bp.route("/api/cart/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    print(data)
    product_id = data.get("product_id")
    
    own_cart = Cart(user_id)
    own_cart.save_item_to_db(product_id, 1) 
    
    return jsonify({"message": "Đã thêm thành công"})

@cart_bp.route("/api/cart/remove/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_cart_item(product_id):
    user_id = get_jwt_identity()
    
    own_cart = Cart(user_id)
    own_cart.remove_item_from_db(product_id)
    
    return jsonify({"message": "Đã xóa sản phẩm"})