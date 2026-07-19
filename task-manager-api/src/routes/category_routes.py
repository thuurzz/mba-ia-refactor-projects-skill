from flask import Blueprint, jsonify, request

from src.controllers.category_controller import CategoryController
from src.middlewares.auth import auth_required

category_bp = Blueprint("categories", __name__)


@category_bp.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(CategoryController.list_categories()), 200


@category_bp.route("/categories", methods=["POST"])
@auth_required
def create_category():
    payload, status_code = CategoryController.create_category(request.get_json())
    return jsonify(payload), status_code


@category_bp.route("/categories/<int:category_id>", methods=["PUT"])
@auth_required
def update_category(category_id):
    return jsonify(CategoryController.update_category(category_id, request.get_json())), 200


@category_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@auth_required
def delete_category(category_id):
    return jsonify(CategoryController.delete_category(category_id)), 200
