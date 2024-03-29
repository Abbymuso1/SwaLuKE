from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'hejjtigndlk djntjr'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    db.init_app(app) #initialise the database - using sqlite

    from .views import views
    from .auth import auth

#how to access the views in the specified folders
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    #looking for a user using the id of the user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app; 

def create_database(app):
     with app.app_context():
       #db.drop_all()
       db.create_all()

