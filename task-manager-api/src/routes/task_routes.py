from flask import Blueprint, jsonify, request

from src.controllers.task_controller import TaskController
from src.middlewares.auth import auth_required

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(TaskController.list_tasks()), 200


@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    return jsonify(TaskController.get_task(task_id)), 200


@task_bp.route("/tasks", methods=["POST"])
@auth_required
def create_task():
    payload, status_code = TaskController.create_task(request.get_json())
    return jsonify(payload), status_code


@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@auth_required
def update_task(task_id):
    return jsonify(TaskController.update_task(task_id, request.get_json())), 200


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@auth_required
def delete_task(task_id):
    return jsonify(TaskController.delete_task(task_id)), 200


@task_bp.route("/tasks/search", methods=["GET"])
def search_tasks():
    return jsonify(TaskController.search_tasks(request.args)), 200


@task_bp.route("/tasks/stats", methods=["GET"])
def task_stats():
    return jsonify(TaskController.task_stats()), 200
