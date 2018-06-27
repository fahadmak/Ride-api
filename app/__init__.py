from flask import Flask
from config import app_config

def create_app(config_name):
    """Creates the application and registers the blueprints 
        with the application
    """
    app = Flask(__name__)  
    app.config.from_object(app_config[config_name])
    from app.request.views import request_app
    from app.ride.views import ride_app
    from app.auth.views import auth_blueprint
    # register_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(ride_app)
    app.register_blueprint(request_app)
    return app
    