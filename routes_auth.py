from flask import Blueprint, request
from extensions import db, bcrypt, limiter
from flask_jwt_extended import create_access_token
from models import User
from utils import valid_email, user_to_dict

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/signup")
@limiter.limit("5 per minute")
def signup():
    data = request.json
    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if not full_name or not email or not password or not confirm_password:
        return {"error": "All fields are required"}, 400

    if not valid_email(email):
        return {"error": "Invalid email format"}, 400

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters"}, 400

    if password != confirm_password:
        return {"error": "Passwords do not match"}, 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return {"error": "Email already registered"}, 400

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(full_name=full_name, email=email, password_hash=password_hash, role="user")
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return {"message": "Signup successful", "token": token, "user": user_to_dict(user)}


@auth_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid credentials"}, 401

    if user.status == "blocked":
        return {"error": "Your account is blocked"}, 403

    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=user.id)
    return {"message": "Login successful", "token": token, "user": user_to_dict(user)}


@auth_bp.post("/admin-login")
@limiter.limit("5 per minute")
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    admin = User.query.filter_by(email=email, role="admin").first()

    if not admin:
        return {"error": "Admin not found"}, 401

    if not bcrypt.check_password_hash(admin.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=admin.id)
    return {"message": "Admin login successful", "token": token, "admin": user_to_dict(admin)}