from flask import Blueprint, request, jsonify, render_template
from model.user import SellerModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_page():
    return render_template('admin.html')

@admin_bp.route('/api/approve/<int:sid>', methods=['POST'])
def api_approve(sid):
    note = request.form.get('note')
    s = SellerModel.set_status(sid, "approved", note=note)
    SellerModel.add_notification(sid, "approved", note or "Approved by admin")
    return jsonify({"ok":True,"seller":s})

@admin_bp.route('/api/reject/<int:sid>', methods=['POST'])
def api_reject(sid):
    reason = request.form.get('reason')
    s = SellerModel.set_status(sid, "rejected", note=reason)
    SellerModel.add_notification(sid, "rejected", reason or "Rejected by admin")
    return jsonify({"ok":True,"seller":s})

@admin_bp.route('/api/manual-check/<int:sid>', methods=['POST'])
def api_manual_check(sid):
    # simulate manual check action
    action = request.form.get('action') 
    note = request.form.get('note')
    if action == 'approve':
        SellerModel.set_status(sid, "approved", note=note)
        SellerModel.add_notification(sid, "approved", note or "Approved by manual check")
    else:
        SellerModel.set_status(sid, "rejected", note=note)
        SellerModel.add_notification(sid, "rejected", note or "Rejected by manual check")
    return jsonify({"ok":True,"seller": SellerModel.get(sid)})

@admin_bp.route('/api/auto-conditions', methods=['POST'])
def api_set_auto_conditions():
    data = request.json or {}
    cond = SellerModel.set_auto_conditions(data)
    return jsonify({"ok":True,"conditions":cond})

@admin_bp.route('/api/notifications', methods=['GET'])
def api_notifications():
    return jsonify(SellerModel.get_notifications())
