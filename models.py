import uuid
from datetime import datetime
from extensions import db

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="user")  # user/admin
    profile_pic = db.Column(db.String(200), default="default.png")

    deposit_balance = db.Column(db.Integer, default=0)
    winning_balance = db.Column(db.Integer, default=0)
    bonus_balance = db.Column(db.Integer, default=0)

    status = db.Column(db.String(20), default="active")  # active/blocked
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    image_url = db.Column(db.String(300), nullable=True)

    title = db.Column(db.String(200), nullable=False)
    per_kill = db.Column(db.Integer, nullable=False)
    prize_pool = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    map = db.Column(db.String(50), nullable=False)

    total_players = db.Column(db.Integer, nullable=False)
    joined_players = db.Column(db.Integer, default=0)

    status = db.Column(db.String(20), default="upcoming")  # upcoming/ongoing/completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Join(db.Model):
    __tablename__ = "joins"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    tournament_id = db.Column(db.String, db.ForeignKey("tournaments.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)


class Withdrawal(db.Model):
    __tablename__ = "withdrawals"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="pending")  # pending/approved/rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)


class Deposit(db.Model):
    __tablename__ = "deposits"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="success")  # success/pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(200), default="Fire Fire Play")
    logo_url = db.Column(db.String(300), default="")
    upi_number = db.Column(db.String(100), default="")