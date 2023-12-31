# Import necessary modules
from . import db  # from . is equivalent to from website, so anything in this package can be imported
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the User class, which inherits from db.Model and UserMixin
class User(db.Model, UserMixin):
    # Define class attributes as columns in the database table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    min_wave_height = db.Column(db.Integer)
    max_wave_height = db.Column(db.Integer)
    max_wind_mph = db.Column(db.Integer)
    min_water_temp = db.Column(db.Integer)
