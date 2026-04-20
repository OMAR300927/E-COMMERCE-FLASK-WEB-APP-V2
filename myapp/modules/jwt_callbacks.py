from flask import redirect, url_for, flash
from ..extension import jwt


# ❌ عندما لا يوجد توكن
@jwt.unauthorized_loader
def missing_token_callback(reason):
    flash("Please log in first", "error")
    return redirect(url_for("users_bp.login"))


# ❌ عندما يكون التوكن غير صالح
@jwt.invalid_token_loader
def invalid_token_callback(reason):
    flash("Invalid token, please log in again", "error")
    return redirect(url_for("users_bp.login"))


# ❌ عندما يكون التوكن منتهي الصلاحية (اختياري لكن مهم)
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    flash("Session expired, please log in again", "error")
    return redirect(url_for("users_bp.login"))