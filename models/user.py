from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)


class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'email', 'password')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])