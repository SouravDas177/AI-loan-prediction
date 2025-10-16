from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()
mail=Mail()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Mail configuration (Gmail example)
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "sourav177official@gmail.com"
    app.config["MAIL_PASSWORD"] = "eesr actj zeit riod"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

    db.init_app(app)

    try:
        from .router.auth import auth_bp
        from .router.home import home_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
    except Exception:
        logging.exception("Failed to import/register blueprints")
        raise
    mail.init_app(app)
    # ✅ Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
