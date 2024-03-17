from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False, unique=True)
    location = db.Column(db.String)