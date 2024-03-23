from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.character import Character
from models.session_tracker import session_schema, SessionTracker
from models.session_loot import SessionLoot


sessions_bp = Blueprint('session_tracker', __name__, url_prefix='/session_tracker')

@sessions_bp.route('/create', methods=["POST"])
@jwt_required()
def create_session():
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
  
@sessions_bp.route('/<int:session_id>', methods=["PUT"])
@jwt_required()
def edit_session(session_id):
  try:
    user_id = get_jwt_identity()  # Get authenticated user ID

    # Validate session ID and ownership (check if session belongs to user)
    session_tracker = SessionTracker.query.get(session_id)
    if not session_tracker or session_tracker.user_id != user_id:
      return jsonify({"error": "Unauthorized or session not found."}), 403

    data = request.get_json()

    # Update session tracker data selectively
    for key, value in data.items():
      if key in ['area_id', 'start_time', 'end_time', 'experience_gain', 'silver_gained']:
        setattr(session_tracker, key, value)

    # Handle loot data update (discussed later)

    # Save changes
    db.session.commit()

    # Return updated session information
    return jsonify(session_schema.dump(session_tracker)), 200

  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while processing your request. Please try again later."}), 400
  
@sessions_bp.route('/')
@jwt_required()
def view_sessions():
  try:
    user_id = get_jwt_identity()
    session_data = db.session.query(
        SessionTracker,
        SessionLoot.quantity
    ).join(
      SessionLoot, SessionTracker.id == SessionLoot.session_tracker_id
  ).filter(SessionTracker.user_id == user_id).all()

    sessions = []
    for session_tracker, quantity in session_data:
      session = {
        'area_id': session_tracker.area_id,
        'start_time': session_tracker.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'end_time': session_tracker.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        'experience_gain': session_tracker.experience_gain,
        'silver_gained': session_tracker.silver_gained,
        'loot': [{'quantity': quantity}]  # Assuming single loot entry per session
      }
      # Add additional loot entries if there's more than one per session
      if len(session_data) > 1 and session_data[0][0] != session_tracker:  # Check for new session
        session['loot'] = []
      session['loot'].append({'quantity': quantity})
      sessions.append(session)

    return render_template('sessions.html', sessions=sessions)

  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while retrieving your sessions. Please try again later."}), 500
  
@sessions_bp.route('/<int:session_id>', methods=["DELETE"])
@jwt_required()
def delete_session(session_id):
  try:
    user_id = get_jwt_identity()
    session_tracker = SessionTracker.query.get(session_id)
    if not session_tracker or session_tracker.user_id != user_id:
      return jsonify({"error": "Unauthorized or session not found."}), 403

    # Delete the session tracker (cascade takes care of loot)
    db.session.delete(session_tracker)
    db.session.commit()

    return jsonify({"message": "Session deleted successfully."}), 200
  except Exception as err:
    print(f"An unexpected error occured: {err}")
    return jsonify({"error": "An error occured while processing your request. Please try again later."}), 500