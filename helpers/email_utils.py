from flask_mail import Message
from __init__ import mail  # імпортуй `mail`, який ініціалізував у app.py
from flask import current_app

def send_email(subject, recipients, body=None, html_body=None):
    try:
        msg = Message(subject=subject, recipients=recipients)
        if html_body:
            msg.html = html_body
        if body:
            msg.body = body
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Помилка при відправці листа: {e}")