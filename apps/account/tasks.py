from apps.generals.send_mail import send_activation_email, send_reset_password_email

from config.celery import app

@app.task
def send_activation_email_task(email, code):
    send_activation_email(email, code)

@app.task
def send_reset_password_email_task(email, reset_token):
    send_reset_password_email(email, reset_token)

