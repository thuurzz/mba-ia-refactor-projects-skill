from src.config.settings import Config
from src.models.order_model import OrderModel
from src.models.product_model import ProductModel
from src.models.user_model import UserModel


class SystemController:
    @staticmethod
    def health():
        return {
            "status": "ok",
            "database": "connected",
            "counts": {
                "produtos": ProductModel.count_all(),
                "usuarios": UserModel.count_all(),
                "pedidos": OrderModel.count_all(),
            },
            "versao": Config.APP_VERSION,
        }
