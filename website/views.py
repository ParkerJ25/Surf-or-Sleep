from flask import Blueprint, render_template # Blueprint allows us to seerate our app out and allows us to have views defined in different files instead of all in the same file 
from flask_login import login_required, current_user

views = Blueprint('views', __name__) # you dont need to name this the same name as your file but it keeps it simple. We defined the name of the Blueprint as 'views' which we also dont have to use the same name but again it makes it more simple


@views.route('/') # whenever we go to the "/" page which is the homepage, the home function will run 
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/about')
@login_required
def about():
    return render_template("about.html", user=current_user)