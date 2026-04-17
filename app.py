import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from extensions import db, jwt, bcrypt, limiter
from models import User
from routes_auth import auth_bp
from routes_user import user_bp
from routes_tournaments import tournament_bp
from routes_wallet import wallet_bp
from routes_admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(tournament_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return {"message": "Fire Fire Play Backend Running 🚀"}

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    with app.app_context():
        db.create_all()

        # Create default admin if not exists
        admin = User.query.filter_by(email="admin@gmail.com", role="admin").first()
        if not admin:
            from extensions import bcrypt
            password_hash = bcrypt.generate_password_hash("admin").decode("utf-8")

            admin_user = User(
                full_name="Admin",
                email="admin@gmail.com",
                password_hash=password_hash,
                role="admin",
                status="active"
            )
            db.session.add(admin_user)
            db.session.commit()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)