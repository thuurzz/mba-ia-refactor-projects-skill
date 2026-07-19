from flask import Blueprint, jsonify, request

from src.controllers.order_controller import OrderController


order_bp = Blueprint("orders", __name__)


@order_bp.get("/pedidos")
def list_all_orders():
    orders = OrderController.list_all_orders()
    return jsonify({"dados": orders, "sucesso": True}), 200


@order_bp.post("/pedidos")
def create_order():
    order = OrderController.create_order(request.get_json())
    return (
        jsonify(
            {"dados": order, "sucesso": True, "mensagem": "Pedido criado com sucesso"}
        ),
        201,
    )


@order_bp.get("/pedidos/usuario/<int:user_id>")
def list_orders_by_user(user_id):
    orders = OrderController.list_orders_by_user(user_id)
    return jsonify({"dados": orders, "sucesso": True}), 200


@order_bp.put("/pedidos/<int:order_id>/status")
def update_order_status(order_id):
    result = OrderController.update_status(order_id, request.get_json())
    return jsonify(result), 200


@order_bp.get("/relatorios/vendas")
def sales_report():
    report = OrderController.sales_report()
    return jsonify({"dados": report, "sucesso": True}), 200
