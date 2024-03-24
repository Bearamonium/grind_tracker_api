from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db, bcrypt
from models.users import User, user_schema, edited_user_schema
from marshmallow.exceptions import ValidationError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.errorhandler(ValidationError)
def marshmallow_verification(err):
    return jsonify({"error": f"A Validation Error has occured: '{err}"}), 403

@auth_bp.errorhandler(IntegrityError)
def psycopg2_not_null_handler(err):
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        return {"error": f"The {err.orig.diag.column_name} is required."}, 403
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return {"error": "This email address or username is already in use. Please either try again with another email address/username, or login."}, 409

# Creates a new user - /auth/register
@auth_bp.route("/register", methods=["POST"])
def user_registration():
    user_reg_info = request.get_json()
    # Creates User object from the collected data above from user's JSON request
    user = User(
        email=user_reg_info.get('email'),
        username=user_reg_info.get('username'),
        password=bcrypt.generate_password_hash(user_reg_info.get('password')).decode('utf-8')
    )
    # Add new user to the database and then commit changes to the session
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

# Handles login requests for users already in the database
@auth_bp.route("/login", methods=["POST"])
def login():
    # Obtain data from the JSON request body
    login_info = request.get_json()
    # Find the specified user with the entered email address
    stmt = db.select(User).filter_by(email=login_info.get('email'))
    user = db.session.scalar(stmt)
    # The below verifies if the user found matches the entered password
    if user and bcrypt.check_password_hash(user.password, login_info.get('password')):
        # Create JWT 
        jwt_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=2))
        # Return token to the user for use
        return {"email": user.email, "token": jwt_token}, 200
    else: 
        # If user doesn't match password or email doesn't match, return an error to the user
        return {"error": "Invalid email or password. Please try again."}, 401
    
@auth_bp.route("/edit", methods=["PATCH", "PUT"])
@jwt_required()
def edit_user_details():
    # Verify user with JWT token
    user_id = get_jwt_identity()
    # Verify user details
    body_data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user: 
        return jsonify({"error": "User details not found. Please try again."}), 404
    
    user.username = body_data.get('username') or user.username,
    user.email = body_data.get('email') or user.email,
    user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8') or user.password

    db.session.commit()

    return jsonify(edited_user_schema.dump(user)), 201

@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    # Verify JWT token
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User details not found. Please try again."}), 400
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Your user details have been deleted successfully. If you would like to use the api again, please re-register."}), 418
