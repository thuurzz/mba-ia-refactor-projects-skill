import logging

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from src.errors import APIError

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        logger.exception("database_error")
        return jsonify({"error": "Erro de persistência"}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception("unexpected_error")
        return jsonify({"error": "Erro interno"}), 500
