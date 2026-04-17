import os
from flask import Blueprint, request, current_app
from flask_jwt_extended import get_jwt_identity
from extensions import db
from models import User
from middleware import user_required
from utils import user_to_dict

user_bp = Blueprint("user", __name__, url_prefix="/api/user")

@user_bp.get("/me")
@user_required
def me():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()
    return {"user": user_to_dict(user)}


@user_bp.put("/profile-pic")
@user_required
def upload_profile_pic():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "Invalid file"}, 400

    filename = f"{uid}_{file.filename}"
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(upload_path)

    user.profile_pic = filename
    db.session.commit()

    return {"message": "Profile picture updated", "profilePic": filename}