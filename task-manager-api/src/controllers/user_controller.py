from src.errors import APIError
from src.extensions import db
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.serialization_service import serialize_task, serialize_user
from src.services.validation_service import validate_user_payload


class UserController:
    @staticmethod
    def list_users():
        return [serialize_user(user) for user in User.list_all()]

    @staticmethod
    def get_user(user_id):
        user = User.find_by_id(user_id)
        if not user:
            raise APIError("Usuário não encontrado", 404)
        return serialize_user(user, include_tasks=True)

    @staticmethod
    def create_user(data):
        payload = validate_user_payload(data)
        if User.find_by_email(payload["email"]):
            raise APIError("Email já cadastrado", 409)

        password = payload.pop("password")
        user = User(**payload)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return serialize_user(user), 201

    @staticmethod
    def update_user(user_id, data):
        user = User.find_by_id(user_id)
        if not user:
            raise APIError("Usuário não encontrado", 404)

        payload = validate_user_payload(data, partial=True)
        email = payload.get("email")
        if email:
            existing = User.find_by_email(email)
            if existing and existing.id != user_id:
                raise APIError("Email já cadastrado", 409)

        password = payload.pop("password", None)
        for field, value in payload.items():
            setattr(user, field, value)
        if password:
            user.set_password(password)

        db.session.commit()
        return serialize_user(user)

    @staticmethod
    def delete_user(user_id):
        user = User.find_by_id(user_id)
        if not user:
            raise APIError("Usuário não encontrado", 404)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuário deletado com sucesso"}

    @staticmethod
    def get_user_tasks(user_id):
        user = User.find_by_id(user_id)
        if not user:
            raise APIError("Usuário não encontrado", 404)
        return [serialize_task(task) for task in user.tasks]

    @staticmethod
    def login(data):
        if not isinstance(data, dict) or not data:
            raise APIError("Dados inválidos", 400)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise APIError("Email e senha são obrigatórios", 400)
        return AuthService.authenticate(email, password)
