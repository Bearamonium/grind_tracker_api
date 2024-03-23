from init import db, ma
from marshmallow import fields

class Loot(db.Model):
    __tablename__ = "loot"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    drop_rate = db.Column(db.Float)
    sale_price = db.Column(db.BigInteger)

    session_loot = db.relationship('SessionLoot', back_populates='loot', cascade='all, delete')

class LootSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'name', 'description', 'drop_rate', 'sale_price')

loot_schema = LootSchema(many=True)
loot_item_schema = LootSchema()