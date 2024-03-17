from init import db, ma
from marshmallow import fields

class Character(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(40), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String, nullable=False)