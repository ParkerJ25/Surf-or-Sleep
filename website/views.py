# Import necessary modules
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Define route for the homepage '/'
@views.route('/')
@login_required  # Require the user to be logged in to access this route
def home():
    return render_template("home.html", user=current_user)

# Define route for the 'about' page
@views.route('/about')
@login_required  # Require the user to be logged in to access this route
def about():
    return render_template("about.html", user=current_user)

# Define route for the 'sign_up' page
@views.route('/sign_up')
def sign_up():
    return render_template("sign_up.html", user=current_user)
