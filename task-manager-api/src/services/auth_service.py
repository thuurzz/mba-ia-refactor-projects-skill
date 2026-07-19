from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from src.errors import APIError
from src.models.user import User


class AuthService:
    @staticmethod
    def _serializer():
        from flask import current_app

        return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    @classmethod
    def issue_token(cls, user):
        return cls._serializer().dumps({"user_id": user.id, "role": user.role})

    @classmethod
    def authenticate(cls, email, password):
        user = User.find_by_email(email.strip().lower())
        if not user or not user.check_password(password):
            raise APIError("Credenciais inválidas", 401)
        if not user.active:
            raise APIError("Usuário inativo", 403)
        return {"message": "Login realizado com sucesso", "user": user.to_dict(), "token": cls.issue_token(user)}

    @classmethod
    def verify_token(cls, token):
        from flask import current_app

        try:
            payload = cls._serializer().loads(
                token,
                max_age=current_app.config["TOKEN_TTL_SECONDS"],
            )
        except SignatureExpired as exc:
            raise APIError("Token expirado", 401) from exc
        except BadSignature as exc:
            raise APIError("Token inválido", 401) from exc

        user = User.find_by_id(payload["user_id"])
        if not user or not user.active:
            raise APIError("Usuário inativo", 403)
        return user
