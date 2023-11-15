import smtplib
from flask import Blueprint, current_app
from website.models import User
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .web_scraper import get_scraped_data

surfEmail = Blueprint('surfEmail', __name__)

@surfEmail.route('/')
def send_emails():
    # Get the Flask app instance
    app = current_app

    # Replace 'your_email@gmail.com' and 'your_password' with your email credentials
    sender_email = 'parkerstephenson00@gmail.com'
    password = 'ahgp vnbn mvlz cdju'

    # Set up the email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Manually push an application context
    with app.app_context():
        # Get scraped data
        scraped_data = get_scraped_data()

        # Construct email body
        email_body = f"AM Wind: {scraped_data['am_wind']}\n" \
                      f"PM Wind: {scraped_data['pm_wind']}\n" \
                      f"AM Wave: {scraped_data['am_wave']}\n" \
                      f"PM Wave: {scraped_data['pm_wave']}\n" \
                      f"Water Temp: {scraped_data['water_temp']}"

        # Get all user emails
        all_user_emails = [user.email for user in User.query.all()]

        # Print all emails
        print("All User Emails:")
        for email in all_user_emails:
            print(email)

        # Send emails to each user
        for email in all_user_emails:
            send_email(server, email, 'Surf Conditions Update', email_body)

    # Quit the server
    server.quit()

    return "Emails Sent!"

def send_email(server, recipient_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = 'parkerstephenson00@gmail.com'
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.send_message(msg)
send_emails()