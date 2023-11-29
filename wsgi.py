from website import create_app
from surfEmail import send_emails

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

    # Start the APScheduler along with the Flask app
    #from surfEmail cv cv import scheduler as surf_email_scheduler
    #surf_email_scheduler.add_job(id="send_emails", func=send_emails, trigger="cron", hour = 19, minute = 1)
