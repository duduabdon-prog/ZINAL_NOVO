from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # hash da senha
    is_admin = db.Column(db.Boolean, default=False)
    access_expires_at = db.Column(db.DateTime, nullable=True)  # None = vitalício
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    clicks = db.relationship("ClickLog", backref="user", lazy=True)

    def is_access_valid(self):
        """Retorna True se o acesso ainda está válido."""
        return self.access_expires_at is None or self.access_expires_at > datetime.utcnow()

    def __repr__(self):
        return f"<User {self.username}>"

class ClickLog(db.Model):
    __tablename__ = "click_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    button_name = db.Column(db.String(50), nullable=False)  # "telegram" ou "compra"
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ClickLog {self.button_name} - User {self.user_id}>"
