import json, os
import config
from datetime import datetime

class SellerModel:
    _data = {"sellers": [], "next_id": 1, "auto_conditions": {"min_username_len": 3, "require_doc": True, "require_email_verified": True}, "notifications": []}

    @classmethod
    def _load(cls):
        try:
            if os.path.exists(config.PERSIST_FILE):
                with open(config.PERSIST_FILE, 'r', encoding='utf-8') as f:
                    cls._data = json.load(f)
        except Exception as e:
            print("load error", e)

    @classmethod
    def _save(cls):
        try:
            with open(config.PERSIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(cls._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("save error", e)

    @classmethod
    def create_seller(cls, username, email, phone=None):
        cls._load()
        seller = {
            "id": cls._data["next_id"],
            "username": username,
            "email": email,
            "phone": phone,
            "email_verified": False,
            "phone_verified": False,
            "documents": [],    # list of file paths
            "shop": {
                "shop_name": "",
                "description": "",
                "avatar": None,
                "banner": None,
                "address": "",
                "policy": ""
            },
            "status": "pending",   # pending, auto_approved, manual_review, approved, rejected
            "created_at": datetime.utcnow().isoformat(),
            "notes": []
        }
        cls._data["sellers"].append(seller)
        cls._data["next_id"] += 1
        cls._save()
        return seller

    @classmethod
    def list_sellers(cls):
        cls._load(); return cls._data["sellers"]

    @classmethod
    def get(cls, sid):
        cls._load()
        for s in cls._data["sellers"]:
            if s["id"] == sid: return s
        return None

    @classmethod
    def add_document(cls, sid, filepath):
        cls._load()
        s = cls.get(sid)
        if not s: return None
        s["documents"].append(filepath)
        cls._save()
        return s

    @classmethod
    def update_shop(cls, sid, **kwargs):
        cls._load()
        s = cls.get(sid)
        if not s: return None
        for k,v in kwargs.items():
            if k in s["shop"]:
                s["shop"][k] = v
        cls._save()
        return s

    @classmethod
    def verify_email(cls, sid):
        cls._load()
        s = cls.get(sid)
        if not s: return None
        s["email_verified"] = True
        cls._save()
        return s

    @classmethod
    def verify_phone(cls, sid):
        cls._load()
        s = cls.get(sid)
        if not s: return None
        s["phone_verified"] = True
        cls._save()
        return s

    @classmethod
    def set_status(cls, sid, status, note=None):
        cls._load()
        s = cls.get(sid)
        if not s: return None
        s["status"] = status
        if note:
            s["notes"].append({"ts": datetime.utcnow().isoformat(), "note": note})
        cls._save()
        return s

    @classmethod
    def autos_check_and_apply(cls, sid):
        cls._load()
        s = cls.get(sid)
        cond = cls._data.get("auto_conditions", {})
        if not s: return None
        ok = True
        if cond.get("require_doc") and len(s["documents"])==0: ok=False
        if cond.get("require_email_verified") and not s.get("email_verified"): ok=False
        if len(s["username"] or "") < cond.get("min_username_len", 1): ok=False
        if ok:
            s["status"] = "auto_approved"
            cls._data["notifications"].append({"to": s["id"], "type":"auto_approved", "message":"Seller auto-approved"})
        else:
            s["status"] = "manual_review"
        cls._save()
        return s

    @classmethod
    def set_auto_conditions(cls, conditions: dict):
        cls._load()
        cls._data["auto_conditions"].update(conditions)
        cls._save()
        return cls._data["auto_conditions"]

    @classmethod
    def add_notification(cls, to_id, msg_type, message):
        cls._load()
        cls._data["notifications"].append({"to":to_id,"type":msg_type,"message":message,"ts":datetime.utcnow().isoformat()})
        cls._save()

    @classmethod
    def get_notifications(cls):
        cls._load(); return cls._data.get("notifications", [])
