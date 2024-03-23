from init import db, ma
from marshmallow import fields

class SessionTracker(db.Model):
    __tablename__ = "session_tracker"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    experience_gain = db.Column(db.Integer)
    silver_gain = db.Column(db.Integer)

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    loot = db.relationship('SessionLoot', backref='session_tracker', cascade='delete-orphan')

class SessionTrackerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'start_time', 'end_time', 'duration', 'experience_gain', 'silver_gain', 'area_id', 'character_id')

session_schema = SessionTrackerSchema()