import logging

from flask import jsonify


logger = logging.getLogger(__name__)


class AppError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class BadRequestError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class UnauthorizedError(AppError):
    status_code = 401


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"erro": error.message, "sucesso": False}), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception("Unhandled application error")
        return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500
