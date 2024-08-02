from datetime import datetime, timezone
from flask_login import UserMixin
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import uuid


class User(UserMixin, db.Model):
    id: so.Mapped[str] = so.MappedColumn(sa.String(64), primary_key=True)
    username: so.Mapped[str] = so.MappedColumn(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.MappedColumn(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    def set_id(self):
        self.id = str(uuid.uuid4())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'timestamp': self.timestamp,
        }

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
        self.set_id()
