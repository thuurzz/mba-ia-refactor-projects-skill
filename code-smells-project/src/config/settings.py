import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
    DB_PATH = os.environ.get("DB_PATH", "loja.db")
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "5000"))
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    APP_VERSION = "1.0.0"
    VALID_CATEGORIES = (
        "informatica",
        "moveis",
        "vestuario",
        "geral",
        "eletronicos",
        "livros",
    )
    VALID_ORDER_STATUSES = (
        "pendente",
        "aprovado",
        "enviado",
        "entregue",
        "cancelado",
    )
