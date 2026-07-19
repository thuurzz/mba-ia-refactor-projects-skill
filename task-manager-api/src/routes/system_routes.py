from flask import Blueprint, jsonify

from src.services.datetime_service import utc_now

system_bp = Blueprint("system", __name__)


@system_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": utc_now().isoformat()}), 200


@system_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Task Manager API", "version": "2.0"}), 200
