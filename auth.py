from flask_jwt_extended import get_jwt_identity
from flask import abort, jsonify
from models.users import User
from models.character import Character
from init import db

def authorise_as_user():
    user_id = int(get_jwt_identity())
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return user
    else: 
        return jsonify({"error": "Your JWT token is incorrect. Please try again."}), 403

def authorise_char_owner(character_id):
    user_id = get_jwt_identity()
    character = Character.query.filter_by(id=character_id, user_id=user_id)
    if character is None:
        return jsonify({"error": "You are not authorised to perform this function."}), 403
    else: 
        return character