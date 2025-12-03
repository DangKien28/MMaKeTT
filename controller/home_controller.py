from flask import Blueprint, render_template, request, jsonify
from model.product import get_all_products, get_product_by_id

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

# --- API ROUTES ---

@home_bp.route('/api/products', methods=['GET'])
def get_products():
    """API Tìm kiếm & Lọc sản phẩm (Epic 1)"""
    products = get_all_products()
    
    # Lấy tham số từ URL
    keyword = request.args.get('keyword', '').lower()
    vendor = request.args.get('vendor', '').lower()
    category = request.args.get('category', '').lower()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    sort_by = request.args.get('sort_by', 'relevance')

    # Logic Lọc
    filtered_products = []
    for p in products:
        match = True
        if keyword and keyword not in p['name'].lower() and keyword not in p['id'].lower(): match = False
        if vendor and p['vendor'].lower() != vendor: match = False
        if category and p['category'].lower() != category: match = False
        if min_price is not None and p['price'] < min_price: match = False
        if max_price is not None and p['price'] > max_price: match = False
        if match: filtered_products.append(p)

    # Logic Sắp xếp
    if sort_by == 'popular': filtered_products.sort(key=lambda x: x['views'], reverse=True)
    elif sort_by == 'newest': filtered_products.sort(key=lambda x: x['release_date'], reverse=True)

    return jsonify({"products": filtered_products, "count": len(filtered_products)})

@home_bp.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """API Gợi ý sản phẩm (Epic 1)"""
    products = get_all_products()
    trending = sorted(products, key=lambda x: x['views'], reverse=True)[:3]
    related = [p for p in products if p['category'] == 'Phụ kiện'][:2]
    behavioral = [p for p in products if p['id'] == 'SP001']
    return jsonify({"trending": trending, "related": related, "behavioral": behavioral})

@home_bp.route('/api/product/<id>', methods=['GET'])
def get_product_detail_api(id):
    """API lấy chi tiết sản phẩm cho Modal (Epic 4 - Mới)"""
    p = get_product_by_id(id)
    if p:
        return jsonify(p)
    return jsonify({"error": "Not found"}), 404

@home_bp.route('/product/<id>')
def product_detail_page(id):
    """MMK-147: Trang chi tiết sản phẩm"""
    product = get_product_by_id(id)
    if not product:
        return "Sản phẩm không tồn tại", 404
        
    if 'images' not in product or not product['images']:
        product['images'] = ["https://via.placeholder.com/500x500?text=No+Image"]
        
    return render_template('product_detail.html', p=product)