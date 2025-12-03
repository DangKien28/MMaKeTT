from flask import Blueprint, request, jsonify, render_template, current_app
from model.user import SellerModel
import os, random
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)

# pages
@auth_bp.route('/register')
def register_page():
    return render_template('register.html')

@auth_bp.route('/verify')
def verify_page():
    return render_template('verify.html')

@auth_bp.route('/upload-doc')
def upload_doc_page():
    return render_template('upload_doc.html')

# APIs
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    if not username or not email:
        return jsonify({"ok":False,"error":"username và email bắt buộc"}),400
    seller = SellerModel.create_seller(username=username, email=email, phone=phone)
    SellerModel.autos_check_and_apply(seller["id"])
    return jsonify({"ok":True,"seller":seller})

@auth_bp.route('/api/send-verify/<int:sid>', methods=['POST'])
def api_send_verify(sid):
    code = random.randint(1000,9999)
    SellerModel.add_notification(sid, "verify_code", f"Your code: {code}")
    return jsonify({"ok":True,"code":code})

@auth_bp.route('/api/verify-email/<int:sid>', methods=['POST'])
def api_verify_email(sid):
    s = SellerModel.verify_email(sid)
    if not s: return jsonify({"ok":False,"error":"seller not found"}),404
    SellerModel.autos_check_and_apply(sid)
    return jsonify({"ok":True,"seller":s})

@auth_bp.route('/api/verify-phone/<int:sid>', methods=['POST'])
def api_verify_phone(sid):
    s = SellerModel.verify_phone(sid)
    if not s: return jsonify({"ok":False,"error":"seller not found"}),404
    SellerModel.autos_check_and_apply(sid)
    return jsonify({"ok":True,"seller":s})

@auth_bp.route('/api/upload-doc/<int:sid>', methods=['POST'])
def api_upload_doc(sid):
    file = request.files.get('document')
    if not file: return jsonify({"ok":False,"error":"no file"}),400
    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    webpath = '/static/images/uploads/' + filename
    SellerModel.add_document(sid, webpath)
    SellerModel.autos_check_and_apply(sid)
    return jsonify({"ok":True,"path":webpath, "seller": SellerModel.get(sid)})
