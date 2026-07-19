import logging


logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    def notify_order_created(order_id, user_id):
        logger.info("Pedido %s criado para usuario %s", order_id, user_id)

    @staticmethod
    def notify_order_status_changed(order_id, status):
        logger.info("Pedido %s atualizado para status %s", order_id, status)
