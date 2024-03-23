from init import db, ma
from marshmallow import fields

class Enemy(db.Model):
    __tablename__ = "enemy"

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    name = db.Column(db.String)
    experience = db.Column(db.Integer)