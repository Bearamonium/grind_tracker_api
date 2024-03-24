# Import flask commands for requesting and returning information along with user authentication
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import errorcodes for error handling
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

# Import SQLAlchemy
from init import db

# Import relevant models
from models.character import Character, character_schema

character_bp = Blueprint('character', __name__, url_prefix='/character')

# Catch specified integrity errors raised through psycopg2 errorcodes Uniqie Violation from the schema and Not Null Violation set in the model and schema
@character_bp.errorhandler(IntegrityError)
def integrity_error_handler(err):
    # Logic to return two separate messages based on the specified error code raised by SQLAlchemy
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return {"error": "Character name is already in use."}, 400
    elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        return {"error": f"The {err.orig.diag.column_name} is required"}, 403

# Catch any Marshmallow validation errors from the CharacterSchema
@character_bp.errorhandler(ValidationError)
def marshmallow_verification(err):
    # Return error messages to user from the CharacterSchema
    return jsonify({"errors": err.messages}), 400

# Creates a new character under username
# POST "/auth/create"
@character_bp.route('/create', methods=["POST"])
@jwt_required()
def create_character():
    # Check if user has a valid JWT token
    user = get_jwt_identity()  # Will return None if no valid token exists

    # User is authenticated
    character_info = request.get_json()

    # Initialise object of CharacterSchema to check data against any possible validation errors from the marshmallow schema
    character_data = character_schema.load(character_info)

    # Chreate character object based on validated information
    character = Character(
        name=character_data.get('name'),
        class_name=character_data.get('class_name'),
        level=character_data.get('level'),
        user_id=user
    )
    # Add character and commit back to the database
    db.session.add(character)
    db.session.commit()

    # Return successfully created character back to user
    return character_schema.dump(character), 201

# Edit character details based on character ID
# PUT, PATCH "/auth/edit/<int:character_id>"
@character_bp.route('/edit/<int:character_id>', methods=["PUT", "PATCH"])
@jwt_required()
def edit_character(character_id):
    user_id = get_jwt_identity()  # Get authenticated user ID
    # Check if character exists for the authenticated user
    character = Character.query.filter_by(id=character_id, user_id=user_id).first()
    if character is None:
        return {"error": "Character not found or you do not have permission to edit it"}, 404

    # Get updated character data from request
    character_info = request.get_json()

    # Validate character data using CharacterSchema
    character_data = character_schema.load(character_info)

    # Update character object with validated data
    character.name = character_data.get('name')
    character.class_name = character_data.get('class_name')
    character.level = character_data.get('level')

    # Commit changes to the database
    db.session.commit()

    # Return successfully edit character details back to user
    return character_schema.dump(character), 201

# Route for deleting character data related to the user's id
# DELETE "/auth/delete/<int:character_id>"
@character_bp.route('/delete/<int:character_id>', methods=["DELETE"])
@jwt_required()
def delete_character(character_id):
    stmt = db.select(Character).where(Character.id==character_id)
    character = db.session.scalar(stmt)

    if character:
        db.session.delete(character)
        db.session.commit()

        return jsonify({"message": f"{character.name} has now been deleted successfully."}), 200
    
    else: 
        return jsonify({"error": f"Character with id {character_id} not found."}), 400

# Route for obtaining a list of all characters associated with the user's id
# GET "/auth/characters"
@character_bp.route('/characters', methods=["GET"])
@jwt_required()
def get_characters():
    user_id = get_jwt_identity()  # Get authenticated user ID

    # Filter characters for the authenticated user
    characters = Character.query.filter_by(user_id=user_id).all()

    # Return list of characters as JSON using character schema for serialization
    return jsonify(character_schema.dump(characters, many=True)), 200



