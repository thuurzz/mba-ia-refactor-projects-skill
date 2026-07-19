from flask import Blueprint, jsonify

from src.controllers.system_controller import SystemController


system_bp = Blueprint("system", __name__)


@system_bp.get("/health")
def health():
    status = SystemController.health()
    return jsonify(status), 200
