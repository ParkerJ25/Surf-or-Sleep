from flask import Flask, render_template # importing flask smd creating a flask web server 
                                         # importing render template lets Flask look for HTML files
                                         # in the templates folder then it renders them 
app = Flask(__name__) # __name__ means this current file which in this case is main.py this 
                      # will represent the flask application

@app.route("/")   # this is the default page for our website 
def home():       # when entering the default page, this function will activate
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":  # When ran Python assigns "__main__" as the name of the script
    app.run(debug=True)     # This runs the application, debug=True lets us see bugs/errors on the webpage




