# Flask imports relevant to making requests and responses
from flask import Blueprint, request, jsonify

# Import SQLAlchemy
from init import db

# Import relevant models & schemas
from models.area import areas_schema, area_schema, Area
from models.enemy import enemies_schema, Enemy
from models.loot import loot_schema, loot_item_schema, Loot

lookup_bp = Blueprint('lookup', __name__, url_prefix='/lookup')

# Route for obtaining all areas, with enemies nested per AreaSchema
@lookup_bp.route('/areas', methods=["GET"])
def get_areas():
    # Obtain information from the database
    stmt = db.select(Area).order_by(Area.name.asc())
    areas = db.session.scalars(stmt)
    # Return result back to the user
    return areas_schema.dump(areas), 200

# Route for obtaining a singular area
@lookup_bp.route('/areas/<int:area_id>', methods=["GET"])
def get_area(area_id):
    # Obtain relevant data from database
    stmt = db.select(Area).filter_by(id=area_id)
    area = db.session.scalar(stmt)
    # Return result to the user if request was found
    if area:
        return area_schema.dump(area)
    # Return error to user notifying them to try a valid id
    else:
        return jsonify({"error": f"Area with the id {area_id} was not found. Please try again with a different id."}), 400

# Route for obtaining list of all enemies sorted in alphabetical order
@lookup_bp.route('/enemies', methods=["GET"])
def get_enemies():
    # Obtain information from the database
    stmt = db.select(Enemy).order_by(Enemy.name)
    enemies = db.session.scalar(stmt)
    # Return result to the user
    return enemies_schema.dump(enemies), 200

# Route for obtaining list of available loot in game - limited model structure so no relationship with enemy or area
@lookup_bp.route('/loot', methods=["GET"])
def get_loot():
    # Obtain information from the database
    stmt = db.select(Loot).order_by(Loot.name.asc())
    loot = db.session.scalar(stmt)
    # Return loot data back to the user
    return loot_schema.dump(loot)

# Route for obtaining one specific loot item
@lookup_bp.route('/loot/<int:loot_id>', methods=["GET"])
def get_loot_item(loot_id):
    # Obtain information from the database
    stmt = db.select(Loot).filter_by(id=loot_id)
    loot_item = db.session.scalar(stmt)
    # Return result to user of loot item exists
    if loot_item: 
        return loot_item_schema.dump(loot_item)
    else: 
        return jsonify({"error": f"Loot with the id {loot_id} was not found. Please try again with a different id."})
    
