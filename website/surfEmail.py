import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from web_scraper import get_scraped_data

def send_email(recipient_email, subject, body):
    # Replace 'your_email@gmail.com' and 'your_password' with your email credentials
    sender_email = 'parkerstephenson00@gmail.com'
    password = 'ahgp vnbn mvlz cdju'

    # Set up the email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.send_message(msg)
    
    # Quit the server
    server.quit()

if __name__ == "__main__":
    # Get scraped data
    scraped_data = get_scraped_data()

    # Construct email body
    email_body = f"AM Wind: {scraped_data['am_wind']}\n" \
                  f"PM Wind: {scraped_data['pm_wind']}\n" \
                  f"AM Wave: {scraped_data['am_wave']}\n" \
                  f"PM Wave: {scraped_data['pm_wave']}\n" \
                  f"Water Temp: {scraped_data['water_temp']}"

    # Send email to yourself
    send_email('surforsleep99@gmail.com', 'Surf Conditions Update', email_body)
