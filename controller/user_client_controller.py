from flask import Blueprint, render_template, request, jsonify

from model.user_client import get_current_user, update_user_profile

user_bp = Blueprint('user', __name__)

# --- VIEW ROUTES ---
@user_bp.route('/profile')
def profile_page():
    """Trang hồ sơ người dùng"""
    user = get_current_user()
    return render_template('profile.html', user=user)

# --- API ROUTES ---
@user_bp.route('/api/user/update', methods=['POST'])
def update_profile_api():
    """MMK-163, 169: API nhận dữ liệu ảnh và thông tin để lưu"""
    data = request.json
    
    if data.get('avatar') and len(data['avatar']) > 3 * 1024 * 1024: 
        return jsonify({"success": False, "message": "Ảnh quá lớn! Vui lòng chọn ảnh dưới 2MB."}), 400

    updated_user = update_user_profile(data)
    
    return jsonify({
        "success": True, 
        "message": "Cập nhật hồ sơ thành công!", 
        "user": updated_user
    })