from flask import Blueprint, jsonify

from src.controllers.report_controller import ReportController
from src.middlewares.auth import auth_required

report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports/summary", methods=["GET"])
@auth_required
def summary_report():
    return jsonify(ReportController.summary_report()), 200


@report_bp.route("/reports/user/<int:user_id>", methods=["GET"])
@auth_required
def user_report(user_id):
    return jsonify(ReportController.user_report(user_id)), 200
