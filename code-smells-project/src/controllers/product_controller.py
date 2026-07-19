from src.config.settings import Config
from src.middlewares.error_handler import BadRequestError, ConflictError, NotFoundError
from src.models.product_model import ProductModel
from src.services.validation_service import validate_product_payload


class ProductController:
    @staticmethod
    def list_products():
        return ProductModel.get_all()

    @staticmethod
    def get_product(product_id):
        product = ProductModel.get_by_id(product_id)
        if not product:
            raise NotFoundError("Produto nao encontrado")
        return product

    @staticmethod
    def create_product(payload):
        data = validate_product_payload(payload, Config.VALID_CATEGORIES)
        product_id = ProductModel.create(**data)
        return {"id": product_id}

    @staticmethod
    def update_product(product_id, payload):
        if not ProductModel.get_by_id(product_id):
            raise NotFoundError("Produto nao encontrado")

        data = validate_product_payload(payload, Config.VALID_CATEGORIES)
        ProductModel.update(product_id, **data)
        return {"sucesso": True, "mensagem": "Produto atualizado"}

    @staticmethod
    def delete_product(product_id):
        if not ProductModel.get_by_id(product_id):
            raise NotFoundError("Produto nao encontrado")

        try:
            ProductModel.delete(product_id)
        except ConflictError:
            raise

        return {"sucesso": True, "mensagem": "Produto deletado"}

    @staticmethod
    def search_products(term, category=None, min_price=None, max_price=None):
        if category and category not in Config.VALID_CATEGORIES:
            raise BadRequestError("Categoria invalida")
        return ProductModel.search(term, category, min_price, max_price)
