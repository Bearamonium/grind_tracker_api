from init import db, ma
from marshmallow import fields
from models.area import Area

class Enemy(db.Model):
    __tablename__ = "enemy"

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    name = db.Column(db.String)
    experience = db.Column(db.Integer)

    location = db.relationship('Area', back_populates='enemies')

class EnemySchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'experience', 'location')

    location = fields.Nested('AreaSchema', exclude=['enemies', 'id'])

enemy_schema = EnemySchema()
enemies_schema = EnemySchema(many=True)

