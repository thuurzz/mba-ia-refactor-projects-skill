from flask import Blueprint, jsonify, request

from src.controllers.user_controller import UserController


user_bp = Blueprint("users", __name__)


@user_bp.get("/usuarios")
def list_users():
    users = UserController.list_users()
    return jsonify({"dados": users, "sucesso": True}), 200


@user_bp.get("/usuarios/<int:user_id>")
def get_user(user_id):
    user = UserController.get_user(user_id)
    return jsonify({"dados": user, "sucesso": True}), 200


@user_bp.post("/usuarios")
def create_user():
    user = UserController.create_user(request.get_json())
    return jsonify({"dados": user, "sucesso": True}), 201


@user_bp.post("/login")
def login():
    user = UserController.login(request.get_json())
    return jsonify({"dados": user, "sucesso": True, "mensagem": "Login OK"}), 200
