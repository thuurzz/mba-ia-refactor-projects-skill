from src.middlewares.error_handler import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)
from src.models.user_model import UserModel
from src.services.auth_service import AuthService
from src.services.validation_service import validate_user_payload


class UserController:
    @staticmethod
    def list_users():
        return UserModel.get_all()

    @staticmethod
    def get_user(user_id):
        user = UserModel.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        return user

    @staticmethod
    def create_user(payload):
        data = validate_user_payload(payload)
        password_hash = AuthService.hash_password(data["senha"])
        try:
            user_id = UserModel.create(data["nome"], data["email"], password_hash)
        except ConflictError:
            raise
        return {"id": user_id}

    @staticmethod
    def login(payload):
        if not payload:
            raise BadRequestError("Dados invalidos")

        email = payload.get("email", "").strip()
        password = payload.get("senha", "")
        if not email or not password:
            raise BadRequestError("Email e senha sao obrigatorios")

        user_record = UserModel.get_auth_record_by_email(email)
        if not user_record or not AuthService.verify_password(password, user_record["senha"]):
            raise UnauthorizedError("Email ou senha invalidos")

        return {
            "id": user_record["id"],
            "nome": user_record["nome"],
            "email": user_record["email"],
            "tipo": user_record["tipo"],
        }
