from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String, nullable=False)