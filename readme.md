# MMORPG Grind Tracker - Black Desert Online example

#### T2A2 Coder Academy

Philip Mills, 2023 October Cohort

## User Guide

To correctly use this API, you will need to firstly ensure that all necessary steps are taken to install and set-up psotgresql along with Python (created with v 3.11). 

To access the api: 

1. Install and set-up new user in postgresql. Ensure this user is given the correct permissions!
2. Create database - mine was called bdo_grind_tracker. 
3. Please view the ".env.sample" file provided in the repository. This will provide you with the necessary information on whay needs to be added for the application to run. Update SQL_DATABASE_URI to match the user you have created in postgres, along with any password used. 
4. **IMPORTANMT**: You need to have the ability to create a python virtual environment. This can be done via the terminal using the following command (bash): ```python3 -m venv .venv```. Once created, you will then need to activate this environment using your terminal: ```source .venv/bin/activate```. Please note for some users this will be instead ```source .venv/Scripts/activate```. 
5. Install requirements in the .txt file - ```pip install -r requirements```. This ensures all necessary informaiton is installed into your newly created venv. 
6. Using the necessary flask commands outlined in the cli_controller.py file, you will need to create and seed the tables with the pre-filled information. 
**PLEASE NOTE** Information included in this API is *not accurate* and is purely for the necessity of relevant data to create this API. Most information sources came directly from Black Desert Online, but liberties were taken with drop rates, sale prices etc. Please don't mistake this informaiton for being accurate. 

Lastly, time to run that flask app! ```flask run```. 

## Identification of the Problem and Need for this API

### Problem:

For hardcore BDO players, manually tracking grinding sessions can be tedious and time-consuming - believe me, I know all too well. It involves recording start and end times (for the losers amongst us), area information, experience and silver gains. This data can be valuable for analyzing progress, identifying efficient grinding spots, and setting goals. However, the manual tracking process is prone to errors and lacks organization. Garmoth.com really is just a beauty isn't it? Yes, the functionality of the base API included does even less than what Garmoth already does, but it's about what it could *become*. 

### Solution:

This API offers **the start** of an automated and streamlined solution for tracking BDO grinding sessions. It allows players to:

- Record session details: Capture start and end times, area information, experience and silver gains efficiently.
Centralized data storage: Sessions are stored in a central database, eliminating the need for manual records or spreadsheets.
- Analytics potential: Players can analyze their data to identify trends, optimize their grinding strategies, and track progress over time once more functionality is added to the API.

### Target Audience:

Hardcore BDO players who value data-driven approaches to improve their gameplay efficiency, and players interested in tracking their progress and analyzing their grinding sessions for personal insights. The idea is to allow easy data viewing for users to then be able to share their stats with others. Yes, there are only 6 areas (the least popular ones too, but they have a spot in my heart), and not much going on data-wise, but this allows you to see

## Why PostgreSQL

Well, that's simple - there is just so much that a relational database has to offer. These things include: 

- Systematic organisation of data: Relational databases as a starting point offer excelent and well maintained data within defined relationships between them. As you can see, currently there are 7 models - and they all share a relationship with one another in one way or another. 

- Normalization of data and tables: Relational databases *enforce* data normalization, which assists in the elimination of redundant data, or floaters (data that no longer has any foreign key relationship, either because it was already deleted or for some other reason). When it comes to managing data accross multiple characters and grind sessions in a large variety of areas, this is crucial in maintaining that integrity of the informaiton being entered into the database. 

- Scalability, Performance & Flexability: SPF-50 anyone? Jokes aside, relational databases have the structures in place to support the growth of a database over time - PostgreSQL in particular can scall well to accommodate more and more data as it's entered over time, along with multiple users accessing data and submitting queries. This assists in keeping with basic ACID principles within database management systems as well - Atomicity, Consistenct, Isolation and Durability. 

- Queries! : With SQL (Structured Query Language), which is the language used for relational databases, it's easy and efficient to perform complex queries to view information from a wide variety of different tables at the same time - pretty neat! This would allow users of the API to easily extract the information they were after, increasing their insight gains from the knowledge of Kamasylvia!

## What's an ORM? 

An ORM refers to an Object-Relational Mapper, which kind of acts like a bridge between an object orientated programming language (for example, Python), and a relational database (PostrgreSQL). The ORM allows for easier integration between the two distinct languages, allowing software designers and engineers to effectively create and produce code to correctly interact with the environment.

Core functionalities of a CRM include: 

- Mapping Objects to Tables
- CRUD (Create, Read, Update and Delete) Operations
- Data Retrieval and Updates (Hydration and Dehydration)
- Creation of Relationships between Objects
- Some ORMS even allow advanced features allowing for custom database queries (Flask!)

The above functionalites all have their hand in creating the benefits that an ORM has to offer. Firstly, ORM's give developers they power over their development productivity - they do so by reducing the amount of code required to actually interact with the database itself. The integration of object-orientated methods allow for this to happen; instead of pure, heavy SQL inputs, we can produce much cleaner and easier to understand code. 

ORMs also reduce the amount of errors being produced by developers and users, as they handle that hard to comprehend translation between the object models themselves and the database schemas. They do this through being able to effecitively migrate errors that would arise from inputting an incorrect SQL query, and providing back more stylised error messages that are easier to understand. 

Thirdly, ORM's provide us with database independance; with ORM's dealing with the major detail of interracting with the database, we are on the other end learning the ORM's code and functionality. This allows users to switch between different relational database systems without causing massive delays in project timeframes with mass edits of project and database code. They provide consitency in terms of objects - ORMs help simplify the actual reasoning behind your code logic, which increasesd your overall dataflow. 

Last but not least, the security enhancements that come built-in with most ORMs can help protect against any potential breaches to a project's integrity; they can automatically protect against SQL injection attacks (inputting massive amounts of data into the database in hopes of corrupting informaiton etc) and escaping out of any potential threatening user inputs from the interface. 

# Endpoint Documentation

## Feature - Authorisation

## POST "auth/register"

- Registers new user in the users table of the database

- Fields for JSON request:

```JSON
"username" : "Enter username here"
"email" : "Enter email here"
"password" : "Enter password here"
```

- Validation points include 

    - id is not changable - assigned as Primary Key (PK).
    - username field is required - defined in the User model. It cannot be longer than 25 characters. 
    - password is also required and defined the the User model
    - email is additionally marked with the nullable=False inherent in SQLAlchemy to ensure this informaiton is added into the database upon creation. 

- Returns "characters" (empty for new users of course), "email", "id" and "username"

## POST "auth/login"

Description: Generates valide JWT access token for user..

Response Format:

JSON object representing the user's details, including:

- email: The user's email address.
- password: the user's password. 

Example Request:

```JSON
GET /auth/login
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
{
	"email": "email@email.com",
	"password": "123456"
}
```


Example Response:

```JSON
{
	"email": "email@email.com",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTI2MzI0NSwianRpIjoiY2JiMjg5YjEtNzI1NS00ZjBmLTg4NmItY2QyMjc1Y2U4ODg4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTEyNjMyNDUsImNzcmYiOiI4Y2QzZWM0Ni01ZmNlLTRlNGYtYWEwOS1lODI0ZGZhNzQ5N2QiLCJleHAiOjE3MTE0MzYwNDV9.6xYB3clL77f-5KeKa8vxQZ6cSDpgPJIkvyQhBvDDkHQ"
}
```

## PATCH PUT "auth/edit"

Description: Authenticates user and allows them to edit their user details.

Body (JSON):

- ```email``` (required, string): Enter either old or new email address
- ```username``` (required, string): Same as above - to ensure integrity we need to ensure all user fields are completed
- ```password``` (required, string): Same as above. 

ResponseFormat:

JSON object representing the newly updated user information.

Example Request:

```JSON
{
	"email": "teapot@outlook.com",
	"username": "Lilliana", 
	"password": "123456"
}
```
Confirmation is received by the user by returning these values if successfully updated. 

## DELETE "auth/delete"

Description: Authenticates user and allows them to delete themselves as a user.

Verification Points: 

- JWT Token is required to perform actions using this route. 

Note no specific id is requested here, as it is all done through JWT verification tools. 

Example Request: 

```JSON
DELETE /auth/delete 
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
```

Example Response: 

```JSON
{
	"message": "Your user details have been deleted successfully. If you would like to use the api again, please re-register."
}
```

## Feature - Characters

## POST "character/create

Description: Allows user to create a character linked to their User ID. 

Body (JSON):

- ```name``` (required, string): Name for the character - names are unique and will return error messages if the same name is entered and it already exists. There is also a character limit of 25 handled by Marshmallow schema validation. 
- ```level``` (required, integer): Character's level in game. 
- ```class``` (required, string): Restrictions have been placed on this entry as well through the Marshmallow schema. Users will only be able to pick on of the 19 available classes as their choice else an error will be raised. 

Response Format: 

JSON object representing the newly created character to the user. 

Example Request: 

```JSON
POST character/create
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
Content-Type: application/json
{
	"name" : "GooGooDolls",
	"level" : "62",
	"class_name" : "Woosa"
}
```

Example Response: 

```JSON
{
	"class_name": "Woosa",
	"id": 1,
	"level": 62,
	"name": "GooGooDolls",
	"session_tracker": [],
	"user": {
		"username": "OwlCryption"
	}
}
```

## PUT PATCH "character/edit/<int:character_id>"

Description: Allows user to edit a previously created character's informaiton. 

Verification Points: 
- JWT Token is required to perform actions using this route. 
- User is verified as owner of the character

Body (JSON) (Same as making a new class):

- ```name``` (required, string): Name for the character - names are unique and will return error messages if the same name is entered and it already exists. There is also a character limit of 25 handled by Marshmallow schema validation. 
- ```level``` (required, integer): Character's level in game. 
- ```class``` (required, string): Restrictions have been placed on this entry as well through the Marshmallow schema. Users will only be able to pick on of the 19 available classes as their choice else an error will be raised. 

Response Format: 

JSON object representing the newly created character to the user. 

Example Request: 

```JSON
POST character/edit/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
Content-Type: application/json
{
	"name" : "OwlLove",
	"class_name" : "Woosa",
	"level" : "65"
}
```

Example Response: 

```JSON
{
	"class_name": "Woosa",
	"id": 1,
	"level": 65,
	"name": "OwlLove",
	"session_tracker": [],
	"user": {
		"username": "OwlCryption"
	}
}
```

## DELETE "character/delete/<int:character_id>"

Description: Authenticates user and user as owner of the specifed character delete themselves as a user.

Verification Points: 

- JWT Token is required to perform actions using this route. 
- User is verified as owner of the character

Example Request: 

```JSON
DELETE /character/delete/5 
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
```

Example Response: 

```JSON
{
	"message": "GooGooDolls has now been deleted successfully."
}
```

## GET "character/characters"

Description: Authenticates user and uses their ID to pull information from the table.

Verification Points: 

- JWT Token is required to perform actions using this route. 
- User is verified as owner of characters. 

Example Request: 

```JSON
GET /character/characters
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
```

Example Response: 

```JSON
[
	{
		"class_name": "Guardian",
		"id": 4,
		"level": 62,
		"name": "Jemima",
		"session_tracker": [
			{
				"id": 4
			},
			{
				"id": 6
			},
			{
				"id": 7
			},
			{
				"id": 5
			}
		],
		"user": {
			"username": "OwlCryption"
		}
	}
]
```

## Feature - Session Tracker

## POST "session_tracker/create"

Description: Creates a new grinding session for the authenticated user.
Request Parameters:

Body (JSON):

- ```start_time``` (required, string in ISO 8601 format): The start time of the grinding session.
- ```end_time``` (required, string in ISO 8601 format): The end time of the grinding session.
- ```duration``` (required, integer): total number of hours (whole)
- ```area_id``` (required, integer): The ID of the grinding area where the session took place.
- ```character_id``` (required, integer): The ID of the character used in the session.
- ```experience_gained``` (required, integer): The amount of experience gained during the session.
- ```silver_gained``` (required, integer): The amount of silver gained during the session.
- ```session_loot``` (required, array of objects): An array of objects representing acquired loot drops. Each loot object should include:
- ```item_id``` (integer): The ID of the loot item.
- ```quantity``` (integer): The quantity of the loot item obtained. Response 

Please note: the ```session_loot``` fields are actually posed into the session_loot table, but done in the same request as the session. 

ResponseFormat:

JSON object representing the newly created grinding session with its details.

Example Request:

```JSON
POST sessions/create
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
Content-Type: application/json

{
    "start_time": "2024-03-25T15:00:00Z",
    "end_time": "2024-03-25T16:00:00Z",
    "area_id": 5,
    "character_id": 2,
    "experience_gained": 456789,
    "silver_gained": 123000,
    "session_loot": [
        {
            "item_id": 10,
            "quantity": 1
        },
        {
            "item_id": 15,
            "quantity": 3
        }
    ]
}
```
This route will then return the updated data to the user in JSON format once successfully patched. 

## PATCH "session_tracker/<int:session_tracker_id>"

Description: Retrieves the session id to be tracked based on user selection. 

Verification: 

- JWT access token is confirmed
- Character ID linked to the Session Tracker chosen is confirmed against the User's JWT access token to ensure they are the owner of that character prior to making any changes to the informaiton. 

Request Parameters (Exactly the same as POST creation):

- ```start_time``` (required, string in ISO 8601 format): The start time of the grinding session.
- ```end_time``` (required, string in ISO 8601 format): The end time of the grinding session.
- ```duration``` (required, integer): total number of hours (whole)
- ```area_id``` (required, integer): The ID of the grinding area where the session took place.
- ```character_id``` (required, integer): The ID of the character used in the session.
- ```experience_gained``` (required, integer): The amount of experience gained during the session.
- ```silver_gained``` (required, integer): The amount of silver gained during the session.
- ```session_loot``` (required, array of objects): An array of objects representing acquired loot drops. Each loot object should include:
- ```item_id``` (integer): The ID of the loot item.
- ```quantity``` (integer): The quantity of the loot item obtained. Response 

Response Format:

JSON object representing the requested grinding session with its details (same structure as the GET Sessions response example for a single session). 

Example Request: 

```JSON
PATCH /session_tracker/4
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
{
	"start_time" : "2024-03-23T08:00:00",
	"end_time" : "2024-03-23T09:02:00",
	"duration" : "27",
	"area_id" : "1", 
	"character_id" : "4",
	"silver_gain" : "2045786",
	"session_loot" : [
		{
		"loot_id" : "1",
		"quantity_obtained" : "12059"
		},
		{
		"loot_id" : "25",
		"quantity_obtained" : "20"
		}
	]
}
```

## GET "session_tracker/character/<<int:character_id>/sessions"

Description: Retrieves the details of all grinding session identified by the ID of the user's character.

Request Parameters:

- character_id (required, integer in URL path): The unique identifier of the user's character.

Response Format:

JSON object representing the requested grinding session with its details (same structure as the GET Sessions response example for a single session). 

Example Request:

```JSON
/sessions/1
Authorization: Bearer <eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4>
```

Example Response:
```JSON
| {
| 	"start_time" : "2024-03-23T08:00:00",
| 	"end_time" : "2024-03-23T09:02:00",
| 	"duration" : 1,
| 	"area_id" : 1, 
| 	"character_id" : 1,
| 	"silver_gain" : 50315489,
| 	"session_loot" : [
| 		{
| 		"loot_id" : 1,
        "quantity_obtained" : 120348
| 		}
| 	]
| }
```

## DELETE "session_tracker/delete/<int:session_tracker_id>"

Description: Authenticates user and uses their ID and character_id to ensure they are able to delete the specified session

Verification Points: 

- JWT Token is required to perform actions using this route. 
- User is verified as owner of characters. 
- Character is verified as FK of the entered session_tracker_id. 

Example Request: 

```JSON
GET /session_tracker/delete/<1>
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4
```

Example Response: 

```JSON
{
	"message": "Session deleted successfully."
}
```

## Feature - Lookup

## GET "/lookup/loot"

Description: Retrieves the details of all loot data available in the database. 

Request Parameters:

- None! Anyone can read this data - only character and user linked inforamtion is locked behind JWT access. 

Response Format:

JSON object returning available loot information

Example Request:

```JSON
/lookup/loot
Authorization: Bearer <eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4>
```

Example Response:
```JSON
...{
	"description": "Vendors would buy this item at a fair price.",
	"drop_rate": 100.0,
	"id": 29,
	"name": "Token of Bravery",
	"sale_price": 12750
}...
```

## GET "lookup/areas/<int:area_id>

Description: Retrieves the details of one specified area through the request.

Request Parameters:

- None! Anyone can read this data - only character and user linked inforamtion is locked behind JWT access. 

Response Format:

JSON object returning available area information.

Example Request:

```JSON
/lookup/areas/5
Authorization: Bearer <eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4>
```

Response would be exactly the same as the previous endpoint as I included the information for only one area.

## GET /lookup/areas

Description: Retrieves the details of all area data available within the database.

Request Parameters:

- None! Anyone can read this data - only character and user linked inforamtion is locked behind JWT access. 

Response Format:

JSON object returning available area information.

Example Request:

```JSON
/lookup/areas
Authorization: Bearer <eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTE3Nzc1OCwianRpIjoiMmViOWNkZGEtMzU1OS00ZGQyLWIyNjUtNzJjZDNjMzFkY2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTExNzc3NTgsImNzcmYiOiJhNjg1YjE4ZC02MzMyLTQ3MTgtOTg2NS0wMGM3MjRiYzlhNTAiLCJleHAiOjE3MTEzNTA1NTh9.nq6cmVYuwoB405Nsrq574jwGZzyH3SV4BwOfSMP69g4>
```

Example Response:
```JSON
[
	{
		"enemies": [
			{
				"experience": 300,
				"id": 36,
				"name": "Cadry Armoured Fighter"
			},
			{
				"experience": 368,
				"id": 37,
				"name": "Cadry Black Mage"
			},
			{
				"experience": 412,
				"id": 38,
				"name": "Cadry Fighter"
			},
			{
				"experience": 695,
				"id": 39,
				"name": "Cadry Summoning Stone"
			},
			{
				"experience": 300,
				"id": 40,
				"name": "Cadry Small Cannon"
			},
			{
				"experience": 300,
				"id": 41,
				"name": "Cadry Ruins Prison"
			},
			{
				"experience": 355,
				"id": 42,
				"name": "Cadry Large Cannon"
			},
			{
				"experience": 1500,
				"id": 43,
				"name": "Cadry Commander"
			},
			{
				"experience": 6000,
				"id": 44,
				"name": "Cadry Chief Gatekeeper"
			}
		],
		"id": 5,
		"location": "Valencia",
		"name": "Cadry Ruins"
	},...continued
```

Note that as Enemies back populates Area, we have included this information in the Schema available to pull this informaiton too - so you get both the area and the enemies associated with it!

# Entity Relationship Diagram & Explaination

![alt text](image.png)

1. User Model: 

    - As you can see above, the User is linked to the Character via a one to many relationship. This means that one user can have multiple characters, but any one character can only belong to one user. 

    - User has an *implicit* relationship with Session_Tracker through Character.

2. Character Model

    - The character model is linked to the Session_Tracker Model again via a one to many relationship, much like user to character. This kept the overall complicity of the database itself quite simple, as it would get out of hand very quickly if we suddenly associated more and more things with character or user. 

3. Enemy Model

    - Again for simplicity, rather than having the Enemy model link directly with the Area, Session_Tracker and Loot Models, Enemy has a many to one relationship with Area.

    This model almost becomes more of a read-only Model; it can't be updated by a normal user, but the user can access it through requests through the ORM.

    - Enemy Model has an *implicit* relationship with Loot through the Session_Tracker model, and with Session_Tracker through the Area Model. 


4.  Area Model

    - This one was nice and small - it ended up becoming more of a joining table between Enemy and Loot via Session_Tracker. 

    - It as a One to Many relationship with Enemy Model (one area can be associated with many enemies), and then a One to Many relationship with Session_Tracker Model as well (one area can be associated with many session trackers, but each session tracker will only be related to one area.)

5. Session_Tracker Model

    - This proved to be the more complex out of the 7 models when preparing the code. Session_Tracker has the following relationships: 

        - Many to One with Area Model
        - Many to One with Character Model
        - Many to May with Session_Loot Model

    - The many to many relationship was made here through a joining table between Loot and Session_Tracker via Session_Loot. It is many to many as the Session_Tracker Model can have many session_loots connected to it, but Session_Loot can be associated with many Session_Tracker Models as well. 

    - This caused a lot of the requests in the ORM to be a bit more complex in terms of separating and then rejoining the two parts when processing queries. 

    - While this only has three direct relationships, the relationship with all other tables in the app are defined implicity through each other. 

6. Session_Loot Model

    - Originally the Session_Loot Model didn't exist, but I decided that I needed to add a gap between Loot and Session Tracker Models. 

    - Session Loot has a many to many relationship with Session Tracker, along with a many to many relationship with Loot as well. 

7. Loot Model

    - This model only has one relationship, and that is with Session Loot. This is a many to many relationship as many Session Loot entries can be associated with more than one Loot item and vice versa. 

    - Although, I will confess that this was the plan, however during implementation it turned into a many to one relationship with Session Loot, as each session loot entry only has one loot item in it. This was due to passing queries in the Session Tracker table that ended up just joining the data together, so there was no need to have more than one item linked with a single Session Loot Entry. 

As a further explaination, below is the code for each of my Models in the file. 

1. User Model & Schema

```python
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    characters = db.relationship('Character', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'characters')

    characters = fields.List(fields.Nested('CharacterSchema', exclude=['user']))

edited_user_schema = UserSchema(exclude=['characters'])
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
```

2. Character Model & Schema

```python
class LimitedChoiceField(fields.String):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices

    def _deserialize(self, value, attr, data, **kwargs) -> Any:
        if value not in self.choices:
            raise ValidationError("Invalid character class. Please choose from the available options.")
        return super()._deserialize(value, attr, data, **kwargs)

class Character(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(15), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String, nullable=False)

    session_tracker = db.relationship('SessionTracker', back_populates='character', cascade='all, delete')
    user = db.relationship('User', back_populates='characters')

class CharacterSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'name', 'level', 'class_name', 'user', 'session_tracker')

    id = fields.Integer()
    name = fields.String(required=True, validate=Length(min=3, max=15, error="Name must be between 3 and 15 characters long."))
    level = fields.Integer(required=True, validate=Range(min=1, max=67, error="Level must be between 1 and 67."))
    class_name = LimitedChoiceField(required=True, choices=["Warrior", "Maegu", "Woosa", "Witch", "Wizard", "Beserker", "Hashashin", "Lahn", "Striker", "Mystic", "Shai", "Corsair", "Maehwa", "Musa", "Valkyrie", "Ranger", "Archer", "Sage", "Scholar", "Guardian"])

    session_tracker = fields.List(fields.Nested('SessionTrackerSchema', only=['id']))
    user = fields.Nested('UserSchema', only=['username'])

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)
```

3. Enemy Model & Schema

```python
class Enemy(db.Model):
    __tablename__ = "enemy"

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    name = db.Column(db.String)
    experience = db.Column(db.Integer)

    location = db.relationship('Area', back_populates='enemies')

class EnemySchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'experience', 'location')

    location = fields.Nested('AreaSchema', exclude=['enemies', 'id'])

enemy_schema = EnemySchema()
enemies_schema = EnemySchema(many=True)
```

4. Area Model & Schema

```python
class Area(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    location = db.Column(db.String)

    enemies = db.relationship('Enemy', back_populates='location', cascade='all, delete')

class AreaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'enemies')      

    id = fields.Integer()
    name = fields.String()
    location = fields.String()
    enemies = fields.List(fields.Nested('EnemySchema', exclude=['location']))

areas_schema = AreaSchema(many=True)
area_schema = AreaSchema()
```

5. Session Tracker Model & Schema

```python
class Loot(db.Model):
    __tablename__ = "loot"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    drop_rate = db.Column(db.Float)
    sale_price = db.Column(db.BigInteger)

    session_loot = db.relationship('SessionLoot', back_populates='loot', cascade='all, delete')

class LootSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'name', 'description', 'drop_rate', 'sale_price')

loot_schema = LootSchema(many=True)
loot_item_schema = LootSchema()
```

6. Session Loot Model & Schema

```python
class SessionTracker(db.Model):
    __tablename__ = "session_tracker"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    experience_gain = db.Column(db.Integer, nullable=False)
    silver_gain = db.Column(db.Integer, nullable=False)

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    session_loot = db.relationship('SessionLoot', back_populates='session_tracker', cascade='all, delete')
    character = db.relationship("Character", back_populates='session_tracker')

class SessionTrackerSchema(ma.Schema):
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    duration = fields.Integer(required=True)
    experience_gain = fields.Integer(required=True)
    silver_gain = fields.Integer(required=True)
    area_id = fields.Integer(required=True)
    character_id = fields.Integer(required=True)

    session_loot = fields.List(fields.Nested('SessionLootSchema', exclude=['session_tracker']))

    class Meta:
        fields=('id', 'start_time', 'end_time', 'duration', 'experience_gain', 'silver_gain', 'area_id', 'character_id', 'session_loot')
        ordered=True
        partial=True

session_schema = SessionTrackerSchema()
sessions_schema = SessionTrackerSchema(many=True)
```

7. Loot Model & Schema

```python
class SessionLoot(db.Model):
    __tablename__ = "session_loot"

    id = db.Column(db.Integer, primary_key=True)
    quantity_obtained = db.Column(db.Integer)

    loot_id = db.Column(db.Integer, db.ForeignKey('loot.id'), nullable=False)
    session_tracker_id = db.Column(db.Integer, db.ForeignKey('session_tracker.id'), nullable=False)

    session_tracker = db.relationship('SessionTracker', back_populates='session_loot')
    loot = db.relationship('Loot', back_populates='session_loot')

class SessionLootSchema(ma.Schema):

    session_tracker = fields.Nested('SessionTrackerSchema', only=['id', 'character_id'])

    class Meta:
        fields = ('id', 'loot_id', 'quantity_obtained', 'session_tracker')

session_loot_schema = SessionLootSchema()
session_loots_schema = SessionLootSchema(many=True)
```

# Third Party Services

- Flask: A lightweight web framework for building Python web applications.
- PostgreSQL: A powerful open-source relational database management system (DBMS).
- SQLAlchemy: An ORM (Object-Relational Mapper) that simplifies interacting with databases in Python.
- Marshmallow: A library for serializing and deserializing data between Python objects and formats like JSON.
- Bcrypt: A library for securely hashing passwords in Python.
- JSON Web Tokens (JWT): A compact, self-contained way for securely transmitting information between parties.
- Psycopg2: A Python library for interacting with PostgreSQL databases.
- dotenv: A library for loading environment variables from a .env file for secure configuration management.

# Task Management 

I won't grandstand here and say that I'm a project management guru. Believe me, I have tried at times to get ahead on things but a majority of the time I'm really bad at overcommitting myself past what I can actually do. There's a lesson to be learnt there somewhere...

But Trello did come in handy for this project.  I basically threw together a quick Kanban board to keep track of the overall API development workflow. 

In the end it was fairly simple; it had lists for things like 'TODO, In Progress, Completed, Wishlist... yeah just the basic components. It wasn't fancy, but it helped me visualize the progress and stay on top of priorities. Trello wasn't the core of the development process, but it was a lightweight way to keep myself organized to a varied degree throughout the development procvess of this API. 

https://trello.com/b/fzXYwZai/api-design-grind-tracker