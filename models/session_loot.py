from init import db, ma
from marshmallow import fields

class SessionLoot(db.Model):
    __tablename__ = "session_loot"

    id = db.Column(db.Integer, primary_key=True)
    quantity_obtained = db.Column(db.Integer)

    loot_id = db.Column(db.Integer, db.ForeignKey('loot.id'), nullable=False)
    session_tracker_id = db.Column(db.Integer, db.ForeignKey('session_tracker.id'), nullable=False)

    session_tracker = db.relationship('SessionTracker', back_populates='session_loot')
    loot = db.relationship('Loot', back_populates='session_loot')

class SessionLootSchema(ma.Schema):

    session_tracker = fields.List(fields.Nested('SessionTrackerSchema'))

    class Meta:
        fields = ('id', 'loot_id', 'quantity_obtained')

session_loot_schema = SessionLootSchema()
session_loots_schema = SessionLootSchema(many=True)