# Import flask commands for rquesting and returning information along with user authentication
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import datetime to hand iso formatting in the below routes
import datetime

# Import SQLAlchemy
from init import db

# Import relevant models into controller
from models.character import Character
from models.session_tracker import session_schema, SessionTracker
from models.session_loot import SessionLoot, session_loots_schema

# Import error codes to create errorhandlers
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

# Import all designated auth functions to enhance code reusability
from auth import *


sessions_bp = Blueprint('session_tracker', __name__, url_prefix='/session_tracker')

# Addresses Marshmallow errors raised
@sessions_bp.errorhandler(DataError)
def marshmallow_error_handling(err):
    # Access specific Marshmallow error details (e.g., field names)
    error_messages = []
    for field, error in err.messages.items():
        error_messages.append(f"{field}: {', '.join(error)}")  # Format error messages for readability

    return jsonify({"error": "Marshmallow Validation Errors:", "details": error_messages}), 400

@sessions_bp.errorhandler(IntegrityError)
def integrity_error_handling(err):
   return jsonify({"error": str(err)}), 400

@sessions_bp.errorhandler(TypeError)
def type_error_handling(err):
   return jsonify({"error": str(err)}), 400

# Route creates a new session linked to the user's character
@sessions_bp.route('/create', methods=["POST"])
@jwt_required()
def create_session():
  # Request data from JSON body
  body_data = request.get_json()

  # Check character validity (if included) - using imported function from auth
  character_id = body_data.get('character_id')
  authorise_char_owner(character_id=character_id)

  # Iterate through body_data to correctly import the informaiton from the JSON body ready to create the session
  session_tracker_data = {key: value for key, value in body_data.items() if key != 'loot'}
  session_tracker = SessionTracker(**session_tracker_data)

  # Save session data to the database as is currently - not comitted yet
  db.session.add(session_tracker)
  db.session.flush()

  # Save loot data 
  for loot_item in body_data['loot']:
    loot_entry = SessionLoot(
      session_tracker_id=session_tracker.id, 
      loot_id=loot_item['loot_id'], 
      quantity_obtained=loot_item['quantity_obtained'])
    db.session.add(loot_entry)

  # Commit all changes
  db.session.commit()

  # Return basic session information
  return jsonify(session_schema.dump(session_tracker)), 201

# Route allows users to edit their session information as long as their character_id links to both their user_id and the related session chosen in the request
# PATCH, "/session_tracker/<int:session_tracker_id>"
@sessions_bp.route('/<int:session_tracker_id>', methods=["PATCH"])
@jwt_required()
def edit_session(session_tracker_id):
  # Query the database to initialise the session data requested
  session = SessionTracker.query.filter_by(id=session_tracker_id).first()

  # If session doesn't exist, return error back to the user
  if not session:
    return jsonify({"error": "Session not found."}), 404
  
  # Authenticate that the user owns the selected character_id
  authorise_char_owner(character_id=session.character_id)

  # Obtain data from JSON request body
  body_data = request.get_json()
  print(body_data)
  # Initialise dictionary with updated values from the request body OR keep the same data as previously if not included in the JSON file. 
  session_tracker_data = {
    'start_time': body_data.get('start_time') or session.start_time,
    'end_time': body_data.get('end_time') or session.end_time,
    'duration': body_data.get('duration') or session.duration,
    'experience_gain': body_data.get('experience_gain') or session.experience_gain,
    'silver_gain': body_data.get('silver_gain') or session.silver_gain,
    'area_id': body_data.get('area_id') or session.area_id,
    'character_id': body_data.get('character_id') or session.start_time
  }

  # Update the data type of start_time and end_time back into fromisoformat so it can be entered into the database
  try:
    session_tracker_data['start_time'] = datetime.datetime.fromisoformat(body_data.get('start_time'))
    session_tracker_data['end_time'] = datetime.datetime.fromisoformat(body_data.get('end_time'))
  except ValueError:
    return jsonify({"error": "Invalid start_time/end_time format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."}), 400
  
  # Use a query statement to find and then update the requested information from the session_tracker table
  SessionTracker.query.filter_by(id=session_tracker_id).update(session_tracker_data)

  loot_data = request.get_json().get('session_loot', [])
  new_loot = []

  # Delete existing session_loot (debatable - took some messing around but this seems to do the trick, nothing is on delete cascade with SessionLoot)
  SessionLoot.query.filter_by(session_tracker_id=session.id).delete()

  # For each item in JSON request, go through and re-add these items back into the database
  for loot_item in loot_data:
    new_loot.append(SessionLoot(
    session_tracker_id=session.id, 
    loot_id = loot_item['loot_id'],
    quantity_obtained = loot_item.get('quantity_obtained')
    ))
    db.session.add_all(new_loot)
    db.session.commit()

  # Return successfully updated session data back to the user
  return jsonify(session_schema.dump(session_tracker_data), session_loots_schema.dump(new_loot)), 201

# Route allows users to view all related sessions linked to one of their character id's
@sessions_bp.route('/character/<int:character_id>/sessions', methods=["GET"])
@jwt_required()
def view_sessions(character_id):
    # Check if character belongs to user
    authorise_char_owner(character_id=character_id)

    # Using a Joined Query, merge data from both SessionTracker and SessionLoot to serialize once determed the session exists
    stmt = db.session.query(SessionTracker).join(SessionLoot).filter(SessionTracker.character_id == character_id)
    sessions_with_loot = stmt.all()

    if not sessions_with_loot:  # Handle case where no sessions are found
        return jsonify({"message": "No sessions found for this character."}), 404

    # Serialize data using marshmallow schemas
    serialized_data = []
    for session in sessions_with_loot:
        session_data = session_schema.dump(session)
        session_data['session_loot'] = session_loots_schema.dump(session.session_loot)  # Access loot data through relationship
        serialized_data.append(session_data)

    return jsonify(serialized_data), 200

# Route allows user to delete sessions logged on their character
@sessions_bp.route('/delete/<int:session_tracker_id>', methods=["DELETE"])
@jwt_required()
def delete_session(session_tracker_id):
  # Query the database to initialise the session data requested
  session = SessionTracker.query.filter_by(id=session_tracker_id).first()
  # If session doesn't exist, return error back to the user
  if not session:
    return jsonify({"error": "Session not found."}), 418
  
  # Authenticate that the user owns the selected character_id
  authorise_char_owner(character_id=session.character_id)

  # Delete the session tracker (cascade takes care of loot)
  db.session.delete(session)
  db.session.commit()

  return jsonify({"message": "Session deleted successfully."}), 200
