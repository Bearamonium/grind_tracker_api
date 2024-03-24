from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    characters = db.relationship('Character', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'characters')

    characters = fields.List(fields.Nested('CharacterSchema', exclude=['user']))

edited_user_schema = UserSchema(exclude=['characters'])
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])