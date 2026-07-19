import logging
import smtplib

from src.errors import APIError

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, host, port, username, password, sender):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sender = sender

    def send_email(self, recipient, subject, body):
        if not all([self.host, self.port, self.username, self.password, self.sender]):
            raise APIError("Serviço de notificação não configurado", 503)

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.sender, recipient, message)
        logger.info("notification_sent recipient=%s subject=%s", recipient, subject)
