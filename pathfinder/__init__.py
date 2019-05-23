#third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import flask_excel as excel
#local imports
from config import app_config

#db variable initialisation
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_object(app_config[config_name])
    app.config['UPLOAD_FOLDER'] = app.config.from_object(app_config['image_config'])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    excel.init_excel(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this Page"
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    Bootstrap(app)
    from pathfinder import model

    #admin
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint,url_prefix='/admin')

    #auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #home
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    #crimes
    from .crimes import crimes as crime_blueprint
    app.register_blueprint(crime_blueprint)
    return app
