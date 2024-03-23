from init import db, ma
from marshmallow import fields

class Loot(db.Model):
    __tablename__ = "loot"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    drop_rate = db.Column(db.Float)
    sale_price = db.Column(db.BigInteger)

