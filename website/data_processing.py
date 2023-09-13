import smtplib
import schedule 
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from website import db
from models import User
from web_scraper import (
    average_water_temp,
    average_wave_height,
    average_wind,
    scrape_swell_info_water_temp,
    scrape_swell_info_wave_heights,
    scrape_swell_info_wind_mph,
    scrape_surf_forecast_water_temp,
    scrape_surf_forecast_wave_height,
    scrape_surf_forecast_wind_mph,
    scrape_surf_captain_water_temp,
    scrape_surf_captain_wave_height,
    scrape_surf_captain_wind_mph,
)

# Define the send_email function here
def send_email(recipient_email, subject, message):
    # Your email credentials
    sender_email = 'parkerstephenson00@gmail.com'  # Your email address
    sender_password = '9954411Pjss'  # Your email password or app-specific password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server and port
        server.starttls()  # Enable TLS
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print(f'Email sent to {recipient_email} successfully')
    except Exception as e:
        print(f'Error sending email to {recipient_email}: {e}')

# Rest of your code...

def data_process():
    am_wave_swell_info, pm_wave_swell_info = scrape_swell_info_wave_heights()
    water_temp_swell_info = scrape_swell_info_water_temp()
    water_temp_surf_forecast = scrape_surf_forecast_water_temp()
    water_temp_surf_captain = scrape_surf_captain_water_temp()
    am_wind_swell_info, pm_wind_swell_info = scrape_swell_info_wind_mph()

    am_wave_surf_forecast, pm_wave_surf_forecast = scrape_surf_forecast_wave_height()
    am_wind_surf_forecast, pm_wind_surf_forecast = scrape_surf_forecast_wind_mph()

    am_wave_surf_captain, pm_wave_surf_captain = scrape_surf_captain_wave_height()
    am_wind_surf_captain, pm_wind_surf_captain = scrape_surf_captain_wind_mph()

    water_temp = average_water_temp(water_temp_swell_info, water_temp_surf_forecast, water_temp_surf_captain)
    am_wave, pm_wave = average_wave_height(am_wave_swell_info, pm_wave_swell_info, am_wave_surf_forecast, pm_wave_surf_forecast, am_wave_surf_captain, pm_wave_surf_captain)
    am_wind, pm_wind = average_wind(am_wind_surf_captain, pm_wind_surf_captain, am_wind_swell_info, pm_wind_swell_info, am_wind_surf_forecast, pm_wind_surf_forecast)

    # Query user preferences from the database
    user_preferences = User.query.all()

    # Assuming you have scraped surf conditions and stored them in variables like below:
    surf_conditions = {
        'water_temp': water_temp,
        'am_wave': am_wave,
        'pm_wave': pm_wave,
        'am_wind': am_wind,
        'pm_wind': pm_wind,
    }

    # Compare user preferences with surf conditions and send emails
    for user in user_preferences:
        # Compare user preferences with surf conditions
        if (
            user.min_water_temp <= surf_conditions['water_temp'] <= user.max_water_temp and
            user.min_wave_height <= surf_conditions['am_wave'] <= user.max_wave_height and
            user.min_wind_speed <= surf_conditions['am_wind'] <= user.max_wind_speed
        ):
            # User preferences match surf conditions, send an email
            subject = 'Good Surfing Conditions'
            message = 'The surf conditions match your preferences. It\'s a good day to go surfing!'
            send_email(user.email, subject, message)
        else:
            # User preferences do not match surf conditions, send a different email
            subject = 'Sleep In Today'
            message = 'The surf conditions do not match your preferences. It\'s a better day for sleeping.'
            send_email(user.email, subject, message)

    # Your existing code to return data
    return water_temp, am_wave, pm_wave, am_wind, pm_wind

if __name__ == "__main__":
    schedule.every().day.at("06:00").do(data_process)
    water_temp, am_wave, pm_wave, am_wind, pm_wind = data_process()
    subject = 'Surf Conditions Report'
    message = f"Water Temp: {water_temp}, AM Wave: {am_wave}, PM Wave: {pm_wave}, AM Wind: {am_wind}, PM Wind: {pm_wind}"
    
    # Now, you can call the send_email function with the subject and message
    send_email('parkerstephenson00@gmail.com', subject, message)
    while True:
        schedule.run_pending()
        time.sleep(1)
