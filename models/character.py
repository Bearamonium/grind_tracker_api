from typing import Any
from init import db, ma
from marshmallow import fields, ValidationError
from marshmallow.validate import Length, Range

class LimitedChoiceField(fields.String):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices

    def _deserialize(self, value, attr, data, **kwargs) -> Any:
        if value not in self.choices:
            raise ValidationError("Invalid character class. Please choose from the available options.")
        return super()._deserialize(value, attr, data, **kwargs)

class Character(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(15), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String, nullable=False)

    session_tracker = db.relationship('SessionTracker', back_populates='character', cascade='all, delete')
    user = db.relationship('User', back_populates='characters')

class CharacterSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'name', 'level', 'class_name', 'user', 'session_tracker')

    id = fields.Integer()
    name = fields.String(required=True, validate=Length(min=3, max=15, error="Name must be between 3 and 15 characters long."))
    level = fields.Integer(required=True, validate=Range(min=1, max=67, error="Level must be between 1 and 67."))
    class_name = LimitedChoiceField(required=True, choices=["Warrior", "Maegu", "Woosa", "Witch", "Wizard", "Beserker", "Hashashin", "Lahn", "Striker", "Mystic", "Shai", "Corsair", "Maehwa", "Musa", "Valkyrie", "Ranger", "Archer", "Sage", "Scholar", "Guardian"])

    session_tracker = fields.List(fields.Nested('SessionTrackerSchema', only=['id']))
    user = fields.Nested('UserSchema', only=['username'])

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)