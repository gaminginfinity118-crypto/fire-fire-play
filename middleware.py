from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from models import User
from extensions import db

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        user = User.query.filter_by(id=user_id).first()
        if not user or user.role != "admin":
            return {"error": "Admin access required"}, 403

        return fn(*args, **kwargs)
    return wrapper


def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"error": "Unauthorized"}, 401

        if user.status == "blocked":
            return {"error": "Your account is blocked"}, 403

        return fn(*args, **kwargs)
    return wrapper