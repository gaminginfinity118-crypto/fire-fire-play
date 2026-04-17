from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from extensions import db
from models import User, Withdrawal, Deposit
from middleware import user_required

wallet_bp = Blueprint("wallet", __name__, url_prefix="/api/wallet")

@wallet_bp.get("/me")
@user_required
def wallet_me():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    return {
        "wallet": {
            "deposit": user.deposit_balance,
            "winning": user.winning_balance,
            "bonus": user.bonus_balance,
            "total": user.deposit_balance + user.winning_balance + user.bonus_balance
        }
    }


@wallet_bp.post("/deposit")
@user_required
def deposit():
    uid = get_jwt_identity()
    data = request.json
    amount = data.get("amount")

    if not amount or int(amount) <= 0:
        return {"error": "Invalid amount"}, 400

    user = User.query.filter_by(id=uid).first()
    user.deposit_balance += int(amount)

    dep = Deposit(user_id=uid, amount=int(amount), status="success")
    db.session.add(dep)
    db.session.commit()

    return {"message": "Deposit successful"}


@wallet_bp.post("/withdraw")
@user_required
def withdraw():
    uid = get_jwt_identity()
    data = request.json
    amount = data.get("amount")

    if not amount or int(amount) <= 0:
        return {"error": "Invalid amount"}, 400

    user = User.query.filter_by(id=uid).first()

    if user.winning_balance < int(amount):
        return {"error": "Not enough winning balance"}, 400

    withdrawal = Withdrawal(user_id=uid, amount=int(amount), status="pending")
    db.session.add(withdrawal)
    db.session.commit()

    return {"message": "Withdrawal request created", "status": "pending"}