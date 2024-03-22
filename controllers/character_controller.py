from flask import Blueprint, request, jsonify
from psycopg2 import errorcodes
from flask_jwt_extended import jwt_required, get_jwt_identity
from jwt import ExpiredSignatureError 
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from init import db, bcrypt
from models.character import Character, character_schema

character_bp = Blueprint('character', __name__, url_prefix='/character')

# Creates a new character under username
@character_bp.route('/create', methods=["POST"])
@jwt_required()
def create_character():
    try:
        # Check if user has a valid JWT token
        user_id = get_jwt_identity()  # Will return None if no valid token exists

        # User is authenticated
        character_info = request.get_json()
        # Initialise object of CharacterSchema to check data against any possible validation errors from the marshmallow schema
        character_data = character_schema.load(character_info)
        # Chreate character object based on validated information
        character = Character(
            name=character_data.get('name'),
            class_name=character_data.get('class_name'),
            level=character_data.get('level'),
            user_id=user_id
        )
        # Add character and commit back to the database
        db.session.add(character)
        db.session.commit()

        # Return successfully created character back to user
        return character_schema.dump(character), 201

    # Catch any Marshmallow validation errors from the CharacterSchema
    except ValidationError as err: 
        # Return error messages to user from the CharacterSchema
        return jsonify({"errors": err.messages}), 400
    # Handle JWT expired error, Integrity Errors through psycopg and basic other Exceptions and return necessary informaiton to the user with error codes. 
    except (ExpiredSignatureError, IntegrityError, Exception) as err:
            if type(err) == ExpiredSignatureError:
                return {"error": "Your access token has expired. Please generate another token and try again."}, 401
            elif type(err) == IntegrityError:
                if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                    return {"error": "Character name is already in use."}, 400
                elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                    return {"error": f"The {err.orig.diag.column_name} is required"}
            else:
                print(f"An unexpected error occured: {err}")
                return jsonify({"error": "An error occured while processing your request. Please try again later."}), 401

# Edit character details based on character ID
@character_bp.route('/edit/<int:character_id>', methods=["PUT", "PATCH"])
@jwt_required()
def edit_character(character_id):
    try:
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

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify({"error": "Character name already exists. Please enter another and try again."})

    except Exception as err:
        print(f"An unexpected error occured: {err}")
        return jsonify({"error": "An error occured while processing your request. Please try again later."}), 400
    
@character_bp.route('/characters', methods=["GET"])
@jwt_required()
def get_characters():
  try:
    user_id = get_jwt_identity()  # Get authenticated user ID

    # Filter characters for the authenticated user
    characters = Character.query.filter_by(user_id=user_id).all()

    # Return list of characters as JSON using character schema for serialization
    return jsonify(character_schema.dump(characters, many=True)), 200

  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while processing your request. Please try again later."}), 400


