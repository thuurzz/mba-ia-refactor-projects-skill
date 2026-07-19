from flask import Blueprint, jsonify, request

from src.controllers.user_controller import UserController
from src.middlewares.auth import auth_required

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(UserController.list_users()), 200


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(UserController.get_user(user_id)), 200


@user_bp.route("/users", methods=["POST"])
def create_user():
    payload, status_code = UserController.create_user(request.get_json())
    return jsonify(payload), status_code


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@auth_required
def update_user(user_id):
    return jsonify(UserController.update_user(user_id, request.get_json())), 200


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@auth_required
def delete_user(user_id):
    return jsonify(UserController.delete_user(user_id)), 200


@user_bp.route("/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    return jsonify(UserController.get_user_tasks(user_id)), 200


@user_bp.route("/login", methods=["POST"])
def login():
    return jsonify(UserController.login(request.get_json())), 200
