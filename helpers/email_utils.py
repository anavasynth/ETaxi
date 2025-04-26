from flask_mail import Message
from __init__ import mail  # імпортуй `mail`, який ініціалізував у app.py
from flask import current_app

def send_email(subject, recipients, body=None, html_body=None):
    msg = Message(subject=subject, recipients=recipients)
    if html_body:
        msg.html = html_body
    else:
        msg.body = body
    mail.send(msg)