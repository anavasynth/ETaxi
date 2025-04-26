# routes/__init__.py
from flask import Flask
from config import Config
from models import db
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    mail.init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes.main import main_bp
    from routes.transfers import transfers_bp
    from routes.payments import payments_bp
    from routes.admin import admin_bp
    from routes.rides import rides_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(transfers_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(rides_bp)

    return app
