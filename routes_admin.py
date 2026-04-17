from flask import Blueprint, request
from extensions import db, bcrypt
from models import User, Tournament, Settings, Withdrawal, Deposit
from middleware import admin_required
from utils import user_to_dict

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.get("/dashboard")
@admin_required
def dashboard():
    total_users = User.query.filter_by(role="user").count()
    total_tournaments = Tournament.query.count()

    total_deposit = db.session.query(db.func.sum(Deposit.amount)).scalar() or 0
    total_withdrawal = db.session.query(db.func.sum(Withdrawal.amount)).scalar() or 0

    return {
        "totalUsers": total_users,
        "totalTournamentCreated": total_tournaments,
        "totalDeposit": total_deposit,
        "totalWithdrawal": total_withdrawal
    }


@admin_bp.post("/create-tournament")
@admin_required
def create_tournament():
    data = request.json

    tournament = Tournament(
        image_url=data.get("imageUrl"),
        title=data.get("title"),
        per_kill=int(data.get("perKill")),
        prize_pool=int(data.get("prizePool")),
        tag=data.get("tag"),
        map=data.get("map"),
        total_players=int(data.get("totalPlayers")),
        joined_players=0,
        status="upcoming"
    )

    db.session.add(tournament)
    db.session.commit()

    return {"message": "Tournament created successfully"}


@admin_bp.get("/users")
@admin_required
def all_users():
    users = User.query.filter_by(role="user").all()
    return {"users": [user_to_dict(u) for u in users]}


@admin_bp.put("/users/block/<uid>")
@admin_required
def block_user(uid):
    user = User.query.filter_by(id=uid).first()
    if not user:
        return {"error": "User not found"}, 404

    user.status = "blocked"
    db.session.commit()
    return {"message": "User blocked successfully"}


@admin_bp.put("/users/unblock/<uid>")
@admin_required
def unblock_user(uid):
    user = User.query.filter_by(id=uid).first()
    if not user:
        return {"error": "User not found"}, 404

    user.status = "active"
    db.session.commit()
    return {"message": "User unblocked successfully"}


@admin_bp.delete("/users/delete/<uid>")
@admin_required
def delete_user(uid):
    user = User.query.filter_by(id=uid).first()
    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}


@admin_bp.get("/settings")
@admin_required
def get_settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings(app_name="Fire Fire Play")
        db.session.add(settings)
        db.session.commit()

    return {
        "settings": {
            "appName": settings.app_name,
            "logoUrl": settings.logo_url,
            "upiNumber": settings.upi_number
        }
    }


@admin_bp.post("/settings")
@admin_required
def save_settings():
    data = request.json

    settings = Settings.query.first()
    if not settings:
        settings = Settings()

    settings.app_name = data.get("appName")
    settings.logo_url = data.get("logoUrl")
    settings.upi_number = data.get("upiNumber")

    db.session.add(settings)
    db.session.commit()

    return {"message": "Settings updated successfully"}