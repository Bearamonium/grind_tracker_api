from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = "session_loot"

    id = db.Column(db.Integer, primary_key=True)
    loot_id = db.Column(db.Integer, db.ForeignKey('loot.id'), nullable=False)
    session_tracker_id = db.Column(db.Integer, db.ForeignKey('session_tracker.id'), nullable=False)
    quantity_obtained = db.Column(db.Integer)