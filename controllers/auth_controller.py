from datetime import timedelta

from flask import Blueprint, request
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError

from init import db, bcrypt
from models.user import User, UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Creates a new user - /auth/register
@auth_bp.route("/register", methods=["POST"])
def user_registration():
    try:
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
        return UserSchema(exclude=["password"]).dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required."}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "This email address is already in use. Please either try again with another email address or login."}, 409

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
        return {"email": user.email, "token": jwt_token}
    else: 
        # If user doesn't match password or email doesn't match, return an error to the user
        return {"error": "Invalid email or password. Please try again."}, 401