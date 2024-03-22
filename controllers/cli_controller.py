from flask import Blueprint

from init import db, bcrypt
from models.area import Area
from models.character import Character
from models.enemy import Enemy
from models.loot import Loot
from models.session_loot import Session_Loot
from models.session_tracker import Session_Tracker
from models.users import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created successfully")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables have now been dropped")

@db_commands.cli.command('seed')
def seed_tables():
    areas = [
        Area(
            name ="Polly's Forest",
            location ="Kamasylvia",
        ),
        Area(
            name ="Manshaum Forest",
            location ="Kamasylvia",
        ),
        Area(
            name ="Sherekhan Necropolis",
            location = "Dreighan",
        ),
        Area(
            name ="Tshira Ruins",
            location = "Dreighan",
        ),
        Area(
            name ="Cadry Ruins",
            location = "Valencia",
        ),
        Area(
            name ="Desert Naga Temple",
            location = "Valencia",
        )
    ]

    db.session.add_all(areas)

    enemies = [
        Enemy(
            area_id=1,
            name="Thief Imp Philums",
            experience=523
        ),
        Enemy(
            area_id=1,
            name="Twinkle-in-the-Dark Mushroom",
            experience=519
        ),
        Enemy(
            area_id=1,
            name="Trumpet Bell Poison Mushroom",
            experience=518
        ),
        Enemy(
            area_id=1,
            name="Cotton Bubble Mushroom",
            experience=151
        ),
        Enemy(
            area_id=1,
            name="Musk Pocket Mushroom",
            experience=312
        ),
        Enemy(
            area_id=1,
            name="Snowflake Poison Mushroom",
            experience=152
        ),
        Enemy(
            area_id=1,
            name="Shadow Poison Mushroom",
            experience=421
        ),
        Enemy(
            area_id=1,
            name="Cloudy Rain Mushroom",
            experience=1002
        ),
        Enemy(
            area_id=1,
            name="Red Skirt Poison Mushroom",
            experience=600
        ),
        Enemy(
            area_id=2,
            name="Manshaum Hut",
            experience=529
        ),
        Enemy(
            area_id=2,
            name="Manshaum Totem",
            experience=400
        ),
        Enemy(
            area_id=2,
            name="Manshaum Narc's Spear",
            experience=400
        ),
        Enemy(
            area_id=2,
            name="Manshaum Fighter",
            experience=523
        ),
        Enemy(
            area_id=2,
            name="Manshaum Hunter",
            experience=425
        ),
        Enemy(
            area_id=2,
            name="Manshaum Warrior",
            experience=511
        ),
        Enemy(
            area_id=2,
            name="Manshaum Shaman",
            experience=325
        ),
        Enemy(
            area_id=2,
            name="Manshaum Great Warrior",
            experience=1098
        ),
        Enemy(
            area_id=2,
            name="Manshaum Charm",
            experience=241
        )
    ]

    db.session.add_all(enemies)

    db.session.commit()

    print("Table information seeded successfully")