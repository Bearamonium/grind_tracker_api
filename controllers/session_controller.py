from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.character import Character
from models.session_tracker import session_schema, SessionTracker
from models.session_loot import SessionLoot

sessions_bp = Blueprint('session_tracker', __name__, url_prefix='/session_tracker')

@sessions_bp.route('/start', methods=["POST"])
@jwt_required()
def start_session():
  try:
    user_id = get_jwt_identity()  # Get authenticated user ID
    data = request.get_json()

    # Validate request data
    session_data, errors = session_schema.load(data)

    if errors:
      return jsonify({"errors": errors}), 400

    # Check character validity (if included)
    character_id = session_data.get('character_id')
    if character_id:
      character = Character.query.filter_by(id=character_id, user_id=user_id).first()
      if not character:
        return jsonify({"error": "Character not found or you do not have permission to use it."}), 400

    # Create new session tracker with user ID and data (excluding loot)
    session_tracker_data = {key: value for key, value in session_data.items() if key != 'loot'}
    session_tracker = SessionTracker(user_id=user_id, **session_tracker_data)

    # Save session tracker data
    db.session.add(session_tracker)

    # Save loot data 
    for loot_item in session_data['loot']:
      loot_entry = SessionLoot(session_tracker_id=session_tracker['id'], loot_id=loot_item['loot_id'], quantity_obtained=loot_item['quantity_obtained'])
      db.session.add(loot_entry)

    # Commit all changes
    db.session.commit()

    # Return basic session information
    return jsonify(session_schema.dump(session_tracker)), 201

  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while processing your request. Please try again later."}), 400