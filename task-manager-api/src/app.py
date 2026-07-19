from flask import Flask
from flask_cors import CORS

from src.config import Config
from src.extensions import db
from src.middlewares import register_error_handlers
from src.routes import category_bp, report_bp, system_bp, task_bp, user_bp
from src.services.logging_service import configure_logging


def create_app():
    configure_logging()

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    app.register_blueprint(system_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(category_bp)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
