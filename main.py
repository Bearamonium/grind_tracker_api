import os

from jwt import ExpiredSignatureError
from werkzeug.exceptions import BadRequest

from flask import Flask, jsonify
from init import db, ma, bcrypt, jwt

def create_app(): 
    app = Flask(__name__)

    # Configurations
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    app.config["JSON_SORT_KEYS"] = False

    @app.errorhandler(ExpiredSignatureError)
    def expired_jwt_token_handler(err):
        return jsonify({"error": f"Your JWT token has expired. Please login in and regenerate a new pass. {err}"})
    
    @app.errorhandler(BadRequest)
    def bad_request_handler(err):
        return jsonify({"error": f"Bad Request, please see details: {err.description}"}), 400

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.character_controller import character_bp
    app.register_blueprint(character_bp)

    from controllers.session_controller import sessions_bp
    app.register_blueprint(sessions_bp)

    from controllers.lookup_controller import lookup_bp
    app.register_blueprint(lookup_bp)

    return app

