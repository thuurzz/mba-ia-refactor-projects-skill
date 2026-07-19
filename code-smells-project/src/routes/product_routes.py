from flask import Blueprint, jsonify, request

from src.controllers.product_controller import ProductController
from src.middlewares.error_handler import BadRequestError


product_bp = Blueprint("products", __name__)


@product_bp.get("/produtos")
def list_products():
    products = ProductController.list_products()
    return jsonify({"dados": products, "sucesso": True}), 200


@product_bp.get("/produtos/busca")
def search_products():
    min_price = _parse_optional_float("preco_min")
    max_price = _parse_optional_float("preco_max")
    products = ProductController.search_products(
        request.args.get("q", "").strip(),
        request.args.get("categoria"),
        min_price,
        max_price,
    )
    return jsonify({"dados": products, "total": len(products), "sucesso": True}), 200


@product_bp.get("/produtos/<int:product_id>")
def get_product(product_id):
    product = ProductController.get_product(product_id)
    return jsonify({"dados": product, "sucesso": True}), 200


@product_bp.post("/produtos")
def create_product():
    product = ProductController.create_product(request.get_json())
    return jsonify({"dados": product, "sucesso": True, "mensagem": "Produto criado"}), 201


@product_bp.put("/produtos/<int:product_id>")
def update_product(product_id):
    result = ProductController.update_product(product_id, request.get_json())
    return jsonify(result), 200


@product_bp.delete("/produtos/<int:product_id>")
def delete_product(product_id):
    result = ProductController.delete_product(product_id)
    return jsonify(result), 200


def _parse_optional_float(param_name):
    value = request.args.get(param_name)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError as error:
        raise BadRequestError(f"{param_name} precisa ser numerico") from error
