from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)  # __name__ means this current file which in this case is __init_.py this 
                           # will represent the flask application
    app.config['SECRET_KEY'] = 'parkerj25'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # we are saying that our SQL alchemy database is stored at 'sqlite:///{DB_NAME}'
    db.init_app(app) # This will take the database and say that this is the app we will be using with this database 

    from.views import views
    from.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User 

    create_database(app) 

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app): # This will check if the database already exists, and if it does not, it will create it 
    if not path.exists('website/' + DB_NAME): # check to see if database exists 
        with app.app_context():
             db.create_all() # if it does not exist we create it 
        print('Created Database!')



