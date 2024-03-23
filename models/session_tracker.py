from init import db, ma
from marshmallow import fields

class SessionTracker(db.Model):
    __tablename__ = "session_tracker"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    experience_gain = db.Column(db.Integer, nullable=False)
    silver_gain = db.Column(db.Integer, nullable=False)

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    session_loot = db.relationship('SessionLoot', back_populates='session_tracker', cascade='all, delete')
    character = db.relationship("Character", back_populates='session_tracker')

class SessionTrackerSchema(ma.Schema):
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    duration = fields.Integer(required=True)
    experience_gain = fields.Integer(required=True)
    silver_gain = fields.Integer(required=True)
    area_id = fields.Integer(required=True)
    character_id = fields.Integer(required=True)

    session_loot = fields.List(fields.Nested('SessionLoot', exclude=['session_tracker']))

    class Meta:
        fields=('id', 'start_time', 'end_time', 'duration', 'experience_gain', 'silver_gain', 'area_id', 'character_id')
        ordered=True

session_schema = SessionTrackerSchema()