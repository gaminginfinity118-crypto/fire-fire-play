from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from extensions import db
from models import Tournament, Join
from middleware import user_required
from utils import tournament_to_dict

tournament_bp = Blueprint("tournaments", __name__, url_prefix="/api/tournaments")

@tournament_bp.get("")
def all_tournaments():
    tournaments = Tournament.query.order_by(Tournament.created_at.desc()).all()
    return {"tournaments": [tournament_to_dict(t) for t in tournaments]}


@tournament_bp.post("/join/<tid>")
@user_required
def join_tournament(tid):
    uid = get_jwt_identity()

    tournament = Tournament.query.filter_by(id=tid).first()
    if not tournament:
        return {"error": "Tournament not found"}, 404

    existing_join = Join.query.filter_by(user_id=uid, tournament_id=tid).first()
    if existing_join:
        return {"error": "Already joined"}, 400

    if tournament.joined_players >= tournament.total_players:
        return {"error": "Tournament is full"}, 400

    join = Join(user_id=uid, tournament_id=tid)
    db.session.add(join)

    tournament.joined_players += 1
    db.session.commit()

    return {"message": "Joined tournament successfully"}


@tournament_bp.get("/my")
@user_required
def my_tournaments():
    uid = get_jwt_identity()

    joins = Join.query.filter_by(user_id=uid).all()
    tournament_ids = [j.tournament_id for j in joins]

    tournaments = Tournament.query.filter(Tournament.id.in_(tournament_ids)).all()
    return {"tournaments": [tournament_to_dict(t) for t in tournaments]}