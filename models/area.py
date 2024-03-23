from init import db, ma
from marshmallow import fields

class Area(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    location = db.Column(db.String)

    enemies = db.relationship('Enemy', back_populates='location', cascade='all, delete')

class AreaSchema(ma.Schema):
    class Meta:
        ordered = True      

    id = fields.Integer()
    name = fields.String()
    location = fields.String()
    enemies = fields.List(fields.Nested('EnemySchema', exclude=['location']))

areas_schema = AreaSchema(many=True)
area_schema = AreaSchema()