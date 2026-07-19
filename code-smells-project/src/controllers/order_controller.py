from src.config.settings import Config
from src.middlewares.error_handler import BadRequestError, NotFoundError
from src.models.order_model import OrderModel
from src.models.user_model import UserModel
from src.services.notification_service import NotificationService


class OrderController:
    @staticmethod
    def create_order(payload):
        if not payload:
            raise BadRequestError("Dados invalidos")

        user_id = payload.get("usuario_id")
        items = payload.get("itens", [])

        if not user_id:
            raise BadRequestError("Usuario ID e obrigatorio")
        if not items:
            raise BadRequestError("Pedido deve ter pelo menos 1 item")
        if not UserModel.exists(user_id):
            raise NotFoundError("Usuario nao encontrado")

        normalized_items = []
        for item in items:
            product_id = item.get("produto_id")
            quantity = item.get("quantidade")
            if not isinstance(product_id, int) or product_id <= 0:
                raise BadRequestError("Item sem produto_id")
            if not isinstance(quantity, int) or quantity <= 0:
                raise BadRequestError("Quantidade deve ser um inteiro positivo")
            normalized_items.append({"produto_id": product_id, "quantidade": quantity})

        order = OrderModel.create(user_id, normalized_items)
        NotificationService.notify_order_created(order["pedido_id"], user_id)
        return order

    @staticmethod
    def list_orders_by_user(user_id):
        if not UserModel.exists(user_id):
            raise NotFoundError("Usuario nao encontrado")
        return OrderModel.get_by_user(user_id)

    @staticmethod
    def list_all_orders():
        return OrderModel.get_all()

    @staticmethod
    def update_status(order_id, payload):
        if not payload:
            raise BadRequestError("Dados invalidos")

        status = payload.get("status", "")
        if status not in Config.VALID_ORDER_STATUSES:
            raise BadRequestError("Status invalido")

        OrderModel.update_status(order_id, status)
        NotificationService.notify_order_status_changed(order_id, status)
        return {"sucesso": True, "mensagem": "Status atualizado"}

    @staticmethod
    def sales_report():
        return OrderModel.sales_report()
