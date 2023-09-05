from website import create_app # since our website folder is now a package we can import it using the name website and by default it will run all of the stuff in the init.py file 

app = create_app()

if __name__ == '__main__': # only if we run this file not if we import it will it run the app.run(debug=True) line of code. We want this because if we imported the main.py file it would run and we only want it to run when we run this file directly
    app.run(debug=True)  # this will run our flask application, start a web server, and debug=true means any change in the python code will rerun the web server
# We are importing website folder as a package(which we can do because we have our __init__.py file, grab the create app function from init.py and use that to create an application and run it)