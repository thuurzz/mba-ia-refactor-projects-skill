from functools import wraps

from flask import g, request

from src.errors import APIError
from src.services.auth_service import AuthService


def auth_required(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        parts = authorization.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise APIError("Autenticação obrigatória", 401)
        g.current_user = AuthService.verify_token(parts[1].strip())
        return handler(*args, **kwargs)

    return wrapper
