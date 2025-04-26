from flask_mail import Message
from __init__ import mail  # імпортуй `mail`, який ініціалізував у app.py
from flask import current_app

def send_email(subject, recipients, body):
    try:
        msg = Message(subject, recipients=recipients, body=body)
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Помилка відправки листа: {e}")