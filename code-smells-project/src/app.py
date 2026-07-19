import logging

from flask import Flask, jsonify
from flask_cors import CORS

from src.config.settings import Config
from src.middlewares.error_handler import register_error_handlers
from src.models.database import init_app as init_database_app
from src.models.database import initialize_database
from src.routes.order_routes import order_bp
from src.routes.product_routes import product_bp
from src.routes.system_routes import system_bp
from src.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"], logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    CORS(app)
    init_database_app(app)
    register_error_handlers(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(system_bp)

    @app.get("/")
    def index():
        return jsonify(
            {
                "mensagem": "Bem-vindo a API da Loja",
                "versao": "1.0.0",
                "endpoints": {
                    "produtos": "/produtos",
                    "usuarios": "/usuarios",
                    "pedidos": "/pedidos",
                    "login": "/login",
                    "relatorios": "/relatorios/vendas",
                    "health": "/health",
                },
            }
        )

    with app.app_context():
        initialize_database()

    return app
