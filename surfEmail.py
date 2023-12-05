# Import necessary modules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from website.models import User
from website.web_scraper import get_scraped_data

# Constants for email scores
IDEAL_SCORE = 3
GOOD_SCORE = 2

# Function to send surf condition emails to users
def send_emails():
    from website import create_app
    app = create_app()  # Assuming create_app() is defined in your website module

    with app.app_context():
        # Set up the email server
        sender_email = 'parkerstephenson00@gmail.com'
        password = 'ahgp vnbn mvlz cdju'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Get scraped data
        scraped_data = get_scraped_data()

        # Go through all users in the database
        for user in User.query.all():
            score = calculate_score(scraped_data, user)

            if score == IDEAL_SCORE:
                email_body = format_email_body("ideal", scraped_data)
            elif score == GOOD_SCORE:
                email_body = format_email_body("good", scraped_data)
            else:
                email_body = format_email_body("not_ideal", scraped_data)

            send_email(server, user.email, 'Surf Conditions Update', email_body)

        # Quit the server
        server.quit()

# Function to calculate the score based on scraped data and user preferences
def calculate_score(scraped_data, user):
    score = 0

    if scraped_data['am_wind'] <= user.max_wind_mph:
        score += 1
    elif scraped_data['am_wind'] <= user.max_wind_mph + 2:
        score += 0
    else:
        score -= 1

    if scraped_data['am_wave'] >= user.min_wave_height and scraped_data['am_wave'] <= user.max_wave_height:
        score += 1
    elif scraped_data['am_wave'] in {user.min_wave_height - 1, user.max_wave_height + 1}:
        score += 0
    else:
        score -= 1

    if scraped_data['water_temp'] > user.min_water_temp:
        score += 1
    elif scraped_data['water_temp'] >= user.min_water_temp + 2:
        score += 0
    else:
        score -= 1

    return score

# Function to format the email body based on surf conditions
def format_email_body(condition_type, scraped_data):
    conditions_dict = {
        "ideal": "It's looking great out there!",
        "good": "Not too bad!",
        "not_ideal": "Sleep in today."
    }

    return f"""
        {conditions_dict[condition_type]} Today's am conditions of {scraped_data['am_wave']} ft waves, 
        a nice water temp of {scraped_data['water_temp']} degrees and winds of {scraped_data['am_wind']} mph 
        are {'ideal for your preferences so get out there and go catch some waves' if condition_type == 'ideal' else 'not in line with your preferences so we suggest going back to bed and resting up for the next good surf!'} \n \n Best Regards, \n your boy P from Surf or Sleep
    """

# Function to send an email
def send_email(server, recipient_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = 'parkerstephenson00@gmail.com'
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.send_message(msg)
