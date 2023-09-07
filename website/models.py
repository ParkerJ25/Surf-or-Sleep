from . import db # from . is equivalent to from website, so anything in this package can be imported
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    min_wave_height = db.Column(db.Integer)
    max_wave_height = db.Column(db.Integer)
    max_wind_mph = db.Column(db.Integer)
    min_water_temp = db.Column(db.Integer)

