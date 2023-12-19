# Import the create_app function from the website package
from website import create_app
# Import the send_emails function from the surfEmail module
from surfEmail import send_emails

# Create the Flask app using the create_app function
app = create_app()

# Check if the script is being run directly
if __name__ == '__main__':
    # Get the PORT environment variable from Heroku, defaulting to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    
    # Run the Flask app in debug mode with reloader turned off
    app.run(debug=True, use_reloader=False, port=port)
