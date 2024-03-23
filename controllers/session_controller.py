from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

from init import db
from models.character import Character
from models.session_tracker import session_schema, SessionTracker
from models.session_loot import SessionLoot, session_loots_schema
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes


sessions_bp = Blueprint('session_tracker', __name__, url_prefix='/session_tracker')

@sessions_bp.route('/create', methods=["POST"])
@jwt_required()
def create_session():
  try:
    user_id = get_jwt_identity()  # Get authenticated user ID
    body_data = request.get_json()

    # Check character validity (if included)
    character_id = body_data.get('character_id')
    if character_id:
      character = Character.query.filter_by(id=character_id, user_id=user_id).first()
      if not character:
        return jsonify({"error": "Character not found or you do not have permission to use it."}), 400

    session_tracker_data = {key: value for key, value in body_data.items() if key != 'loot'}
    session_tracker = SessionTracker(**session_tracker_data)

    # Save session tracker data
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

  except (DataError, TypeError) as err:
    if err.orig.pgcode == errorcodes.DATETIME_FIELD_OVERFLOW:
      return jsonify({"error": "Start and End times need to be in the correct format (ISO Formatting) - YYYY-MM-DDTHH:mm:ss. Please note the T is used as a divider between the date and the time. Example entry: 2024-03-22T08:03:22"})
    if TypeError:
      return jsonify({"error" : "You have entered an invalid data-type for one of your entries. Please refer to the README.MD for further detail."})
  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while processing your request. Please try again later."}), 400
  
@sessions_bp.route('/<int:session_tracker_id>', methods=["PATCH"])
@jwt_required()
def edit_session(session_tracker_id):
  # Obtain data from JSON request body
  body_data = request.get_json()
  try:
    # Query the database to initialise the session data requested
    session = SessionTracker.query.filter_by(id=session_tracker_id).first()

    # If session doesn't exist, return error back to the user
    if not session:
      return jsonify({"error": "Session not found."}), 404
    
    # Authenticate that the user owns the selected character_id
    character = Character.query.filter_by(id=session.character_id).first()
    if not character or character.user_id != int(get_jwt_identity()):
      return jsonify({"error": "Character not found or you do not have permission to use it."}), 403

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
    new_start_time_str = body_data.get('start_time')
    new_end_time_str = body_data.get('end_time')
    try:
      new_start_time = datetime.datetime.fromisoformat(new_start_time_str)
      new_end_time = datetime.datetime.fromisoformat(new_end_time_str)
    # Return Error back to the user if their inputted data is unable to be converted using the above code block. 
    except ValueError:
      return jsonify({"error": "Invalid start_time/end_time format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."})
    # Update data in holding variable to the new isoformatted data
    session_tracker_data['start_time'] = new_start_time
    session_tracker_data['end_time'] = new_end_time
    # Use a query statement to find and then update the requested information from the session_tracker table
    SessionTracker.query.filter_by(id=session_tracker_id).update(session_tracker_data)

    loot_data = request.get_json().get('loot', [])
    new_loot = []

    # Delete existing session_loot
    SessionLoot.query.filter_by(session_tracker_id=session.id).delete()

    for loot_item in loot_data:
      new_loot.append(
        SessionLoot(
          session_tracker_id=session.id, 
          loot_id = loot_item['loot_id'],
          quantity_obtained = loot_item.get('quantity_obtained')
      )
    )
      db.session.add_all(new_loot)
      db.session.commit()
    # Return successfully updated session data back to the user
    return jsonify(session_schema.dump(session_tracker_data), session_loots_schema.dump(new_loot))

  # Catch specified errors below and inform the user of what they need to correct
  except (IntegrityError, DataError) as err:
    if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
      return jsonify({'error': f"Character with id {body_data['character_id']} not found or you do not have permission to use it. Please try again."})
    elif err.orig.pgcode == errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
      return jsonify({'error': "One of your entered values is too high. Please reduce the count and try again."})
    elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return jsonify({"error": "One or more of the required fields are missing a value. Please check to ensure you have included area_id and character_id in your request. Additionally, please ensure there are no spelling errors in your request."})
    elif err.orig.pgcode == errorcodes.DATATYPE_MISMATCH:
      return jsonify({"error": "Please double check all values and data has been entered with the correct values and nothing has been left blank."})
    else:
      return jsonify({'error': "Please refer to the README for correct data value inputs in your request."})
  # Catch all other errors and print it on the terminal back to the user as a Server Error
  except Exception as err:
      print(f"An unexpected error occured: {err}")
      return jsonify({"error": "An internal server error occurred."}), 500

@sessions_bp.route('/character/<int:character_id>/sessions', methods=["GET"])
@jwt_required()
def view_sessions(character_id):
  # Check if character belongs to user
  character = Character.query.get(character_id)
  if not character or character.user_id != int(get_jwt_identity()):
    return jsonify({'error': f"Character with id {character_id} not found or you do not have permission to use it. Please try again."})
  
  # Filter sessions based on the verified user's character
  sessions = SessionTracker.query.join(SessionLoot).filter(SessionTracker.character_id==character_id).all()

  return jsonify(session_schema.dump(sessions, many=True))
  
@sessions_bp.route('/delete/<int:session_tracker_id>', methods=["DELETE"])
@jwt_required()
def delete_session(session_tracker_id):
  try:
    # Query the database to initialise the session data requested
    session = SessionTracker.query.filter_by(id=session_tracker_id).first()

    # If session doesn't exist, return error back to the user
    if not session:
      return jsonify({"error": "Session not found."}), 404
    
    # Authenticate that the user owns the selected character_id
    character = Character.query.filter_by(id=session.character_id).first()
    if not character or character.user_id != int(get_jwt_identity()):
      return jsonify({"error": "Character not found or you do not have permission to use it."}), 403

    # Delete the session tracker (cascade takes care of loot)
    db.session.delete(session)
    db.session.commit()

    return jsonify({"message": "Session deleted successfully."}), 200
  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while processing your request. Please try again later."}), 500