# Import necessary modules and classes
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create the Flask application
def create_app():
    app = Flask(__name__)  # Create a Flask application instance (__name__ represents the current file)

    scheduler = APScheduler()
    scheduler.init_app(app)

    # Add other schedulers if needed
    from surfEmail import send_emails as surf_send_emails  # Rename to avoid confusion
    scheduler.add_job(id="send_emails", func=surf_send_emails, trigger="cron", hour = 6, minute = 1)
    # Start the scheduler
    print("loaded scheduler")
    scheduler.start()

    # Set Flask application configurations
    app.config['SECRET_KEY'] = 'parkerj25'  # Set the secret key for session security
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Set the URI for the SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Set the mail server for Flask-Mail
    app.config['MAIL_PORT'] = 587  # Set the mail server port for Flask-Mail
    app.config['MAIL_USE_TLS'] = True  # Use TLS for Flask-Mail
    app.config['MAIL_USERNAME'] = 'parkerstephenson00@gmail.com'  # Set the email username for Flask-Mail
    app.config['MAIL_PASSWORD'] = 'ahgp vnbn mvlz cdju'  # Set the email password for Flask-Mail
    app.config['MAIL_DEFAULT_SENDER'] = ('Parker Stephenson', 'parkerstephenson@gmail.com')  # Set the default sender for Flask-Mail
    mail = Mail(app)  # Initialize Flask-Mail

    # Initialize SQLAlchemy with the Flask application instance
    db.init_app(app)

    # Initialize Flask-Migrate with the Flask application and SQLAlchemy database instance
    migrate = Migrate(app, db) 

    # Import and register blueprints for different parts of the application
    from.views import views
    from.auth import auth
    #from.surfEmail import surfEmail
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    #app.register_blueprint(surfEmail, url_prefix='/')

    # Import the User model from the models module
    from .models import User 

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login view for Flask-Login
    login_manager.init_app(app)

    # Define a user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the configured Flask application
    return app

# Function to create the database if it does not exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):  # Check if the database file exists
        with app.app_context():
            db.create_all()  # Create all tables in the database
        print('Created Database!')
