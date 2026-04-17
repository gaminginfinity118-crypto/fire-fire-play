import re

def valid_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def user_to_dict(user):
    return {
        "uid": user.id,
        "fullName": user.full_name,
        "email": user.email,
        "role": user.role,
        "profilePic": user.profile_pic,
        "wallet": {
            "deposit": user.deposit_balance,
            "winning": user.winning_balance,
            "bonus": user.bonus_balance
        },
        "status": user.status,
        "createdAt": str(user.created_at)
    }

def tournament_to_dict(t):
    return {
        "id": t.id,
        "imageUrl": t.image_url,
        "title": t.title,
        "perKill": t.per_kill,
        "prizePool": t.prize_pool,
        "tag": t.tag,
        "map": t.map,
        "totalPlayers": t.total_players,
        "joinedPlayers": t.joined_players,
        "status": t.status,
        "createdAt": str(t.created_at)
    }