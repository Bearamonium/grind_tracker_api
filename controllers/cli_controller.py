from flask import Blueprint

from init import db, bcrypt
from models.area import Area
from models.character import Character
from models.enemy import Enemy
from models.loot import Loot
from models.session_loot import SessionLoot
from models.session_tracker import SessionTracker
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
        ),
        Enemy(
            area_id=3,
            name="Federik",
            experience=700
        ),
        Enemy(
            area_id=3,
            name="Nybrica",
            experience=700
        ),
        Enemy(
            area_id=3,
            name="Belcadas",
            experience=700
        ),
        Enemy(
            area_id=3,
            name="Lateh",
            experience=700
        ),
        Enemy(
            area_id=3,
            name="Garud",
            experience=700
        ),
        Enemy(
            area_id=4,
            name="Tree Ghost Spider",
            experience=241
        ),
        Enemy(
            area_id=4,
            name="Swamp Imp Bronk",
            experience=250
        ),
        Enemy(
            area_id=4,
            name="Vine Keeper",
            experience=315
        ),
        Enemy(
            area_id=4,
            name="Grove Keeper",
            experience=500
        ),
        Enemy(
            area_id=4,
            name="Leaf Spider",
            experience=241
        ),
        Enemy(
            area_id=4,
            name="Murky Swamp Caller",
            experience=412
        ),
        Enemy(
            area_id=4,
            name="Leaf Keeper",
            experience=400
        ),
        Enemy(
            area_id=4,
            name="Kvariak",
            experience=8000
        ),
        Enemy(
            area_id=4,
            name="Bronk Huts",
            experience=241
        ),
        Enemy(
            area_id=4,
            name="Bronk Food Storages",
            experience=241
        ),
        Enemy(
            area_id=4,
            name="Venomous Swamp Nest",
            experience=500
        ),
        Enemy(
            area_id=4,
            name="Tree Hermit",
            experience=487
        ),
        Enemy(
            area_id=5,
            name="Cadry Armoured Fighter",
            experience=300
        ),
        Enemy(
            area_id=5,
            name="Cadry Black Mage",
            experience=368
        ),
        Enemy(
            area_id=5,
            name="Cadry Fighter",
            experience=412
        ),
        Enemy(
            area_id=5,
            name="Cadry Summoning Stone",
            experience=695
        ),
        Enemy(
            area_id=5,
            name="Cadry Small Cannon",
            experience=300
        ),
        Enemy(
            area_id=5,
            name="Cadry Ruins Prison",
            experience=300
        ),
        Enemy(
            area_id=5,
            name="Cadry Large Cannon",
            experience=355
        ),
        Enemy(
            area_id=5,
            name="Cadry Commander",
            experience=1500
        ),
        Enemy(
            area_id=5,
            name="Cadry Chief Gatekeeper",
            experience=6000
        )
    ]

    db.session.add_all(enemies)

    loot = [
        Loot(
            name = "Mushroom Hypha",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 100.0,
            sale_price = 9720
        ),
        Loot(
            name = "Atanis' Element",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 5.0,
            sale_price = 39354838
        ),
        Loot(
            name = "Caphras Stone",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 10.0,
            sale_price = 1920000
        ),
        Loot(
            name = "Ancient Spirit Dust",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 6.0,
            sale_price = 302600
        ),
        Loot(
            name = "Life Spirit Stone",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 10.0,
            sale_price = 870000
        ),
        Loot(
            name = "Any Artifact",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 1.0,
            sale_price = 14475000
        ),
        Loot(
            name = "Black Stone (Weapon)",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 5.0,
            sale_price = 291000
        ),
        Loot(
            name = "Black Stone (Armour)",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 5.0,
            sale_price = 200000
        ),
        Loot(
            name = "Pure Forest Breath",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 2.5,
            sale_price = 2910000
        ),
        Loot(
            name = "Trace of Forest",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 10.0,
            sale_price = 231000
        ),
        Loot(
            name = "Imperfect Lightstone of Wind",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 4.5,
            sale_price = 3020000
        ),
        Loot(
            name = "Specter's Energy",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 1.0,
            sale_price = 30000000
        ),
        Loot(
            name = "Manshaum Voodoo Doll",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 10.0,
            sale_price = 680000
        ),
        Loot(
            name = "Manos Craftsman's Clothes",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.2,
            sale_price = 129000000
        ),
        Loot(
            name = "Lemoria Armour",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 8.0,
            sale_price = 970000
        ),
        Loot(
            name = "Water Spirit Stone Fragment",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 20.2,
            sale_price = 50000
        ),
        Loot(
            name = "Lemoria Shoes",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 8.0,
            sale_price = 970000
        ),
        Loot(
            name = "Dew of Tranquil Forest",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 27.2,
            sale_price = 100000
        ),
        Loot(
            name = "Imperfect Lightstone of Fire",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 4.5,
            sale_price = 3020000
        ),
        Loot(
            name = "Imperfect Lightstone of Earth",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 4.5,
            sale_price = 3020000
        ),
        Loot(
            name = "Mass of Pure Magic",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 5.0,
            sale_price = 50000
        ),
        Loot(
            name = "Great Marni's Stone (Polly's Forest)",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.2,
            sale_price = 0
        ),
        Loot(
            name = "Narc Magic Mark",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 100.0,
            sale_price = 12770
        ),
        Loot(
            name = "Narc's Solace",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 1.0,
            sale_price = 45000000
        ),
        Loot(
            name = "Ancient Narc's Crimson Tear",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.1,
            sale_price = 4500000000
        ),
        Loot(
            name = "Lemoria Gloves",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 8.0,
            sale_price = 970000
        ),
        Loot(
            name = "Lemoria Shoes",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 8.0,
            sale_price = 970000
        ),
        Loot(
            name = "Great Marni's Stone (Manshaum)",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.2,
            sale_price = 0
        ),
        Loot(
            name = "Token of Bravery",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 100.0,
            sale_price = 12750
        ),
        Loot(
            name = "Garmoth's Scale",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 1.0,
            sale_price = 3780000
        ),
        Loot(
            name = "Dragon Scale Fossil",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 15.2,
            sale_price = 406000
        ),
        Loot(
            name = "Trace of Battle",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 25.2,
            sale_price = 202200
        ),
        Loot(
            name = "Orkinrad's Belt",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.5,
            sale_price = 9600000
        ),
        Loot(
            name = "Akum Armour",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 4.5,
            sale_price = 970000
        ),
        Loot(
            name = "Great Marni's Stone (Shrekhan - Day)",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.2,
            sale_price = 0
        ),
        Loot(
            name = "Great Marni's Stone (Tshira Ruins)",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.2,
            sale_price = 0
        ),
        Loot(
            name = "Katzvariak's Venom",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 1.0,
            sale_price = 45000000
        ),
        Loot(
            name = "Swamp Leaves",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 100.0,
            sale_price = 8820
        ),
        Loot(
            name = "Ancient Markthanan's Gland",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.1,
            sale_price = 4500000000
        ),
        Loot(
            name = "Eye of the Ruins Ring",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.5,
            sale_price = 25500000
        ),
        Loot(
            name = "Mud Stained Branch",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 85.0,
            sale_price = 4902
        ),
        Loot(
            name = "Cadry's Token",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 100.0,
            sale_price = 15700
        ),
        Loot(
            name = "Ring of Cadry Guardian",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 0.5,
            sale_price = 43300000
        ),
        Loot(
            name = "Scroll Written in Ancient Langage",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 5.2,
            sale_price = 2860000
        ),
        Loot(
            name = "Sealed Black Magic Crystal",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 5.2,
            sale_price = 1230000
        ),
        Loot(
            name = "Yona's Fragment",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 6.2,
            sale_price = 50000
        ),
        Loot(
            name = "Serap's Necklace",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 2.5,
            sale_price = 4970000
        ),
        Loot(
            name = "Trace of Death",
            description = "Vendors would buy this item at a fair price.", 
            drop_rate = 25.2,
            sale_price = 106000
        )
    ]

    db.session.add_all(loot)

    db.session.commit()

    print("Table information seeded successfully")