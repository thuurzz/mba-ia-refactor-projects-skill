"""Script para popular o banco com dados iniciais."""
import logging
from datetime import timedelta

from app import app
from database import db
from src.models import Category, Task, User
from src.services.datetime_service import utc_now

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def seed_data():
    with app.app_context():
        Task.query.delete()
        User.query.delete()
        Category.query.delete()
        db.session.commit()

        users = [
            ("João Silva", "joao@email.com", "12345678", "admin"),
            ("Maria Santos", "maria@email.com", "abcd1234", "user"),
            ("Pedro Oliveira", "pedro@email.com", "pass1234", "manager"),
        ]
        created_users = []
        for name, email, password, role in users:
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            created_users.append(user)
        db.session.commit()

        categories = [
            ("Backend", "Tarefas de backend", "#3498db"),
            ("Frontend", "Tarefas de frontend", "#2ecc71"),
            ("DevOps", "Tarefas de infraestrutura", "#e74c3c"),
            ("Bug", "Correção de bugs", "#e67e22"),
        ]
        created_categories = []
        for name, description, color in categories:
            category = Category(name=name, description=description, color=color)
            db.session.add(category)
            created_categories.append(category)
        db.session.commit()

        now = utc_now()
        tasks_data = [
            {
                "title": "Implementar autenticação JWT",
                "description": "Adicionar autenticação real com JWT",
                "status": "pending",
                "priority": 1,
                "user_id": created_users[0].id,
                "category_id": created_categories[0].id,
                "due_date": now - timedelta(days=3),
            },
            {
                "title": "Criar tela de login",
                "description": "Tela de login responsiva",
                "status": "in_progress",
                "priority": 2,
                "user_id": created_users[1].id,
                "category_id": created_categories[1].id,
                "due_date": now + timedelta(days=5),
            },
            {
                "title": "Configurar CI/CD",
                "description": "Pipeline com GitHub Actions",
                "status": "done",
                "priority": 2,
                "user_id": created_users[2].id,
                "category_id": created_categories[2].id,
                "tags": "devops,ci,github",
            },
            {
                "title": "Corrigir bug no filtro de busca",
                "description": "Filtro não funciona com caracteres especiais",
                "status": "pending",
                "priority": 1,
                "user_id": created_users[0].id,
                "category_id": created_categories[3].id,
                "due_date": now - timedelta(days=1),
            },
            {
                "title": "Adicionar paginação na API",
                "description": "Endpoints retornam todos os registros",
                "status": "pending",
                "priority": 3,
                "user_id": created_users[0].id,
                "category_id": created_categories[0].id,
                "due_date": now + timedelta(days=10),
            },
            {
                "title": "Escrever testes unitários",
                "description": "Cobertura mínima de 80%",
                "status": "pending",
                "priority": 2,
                "user_id": created_users[1].id,
                "category_id": created_categories[0].id,
            },
            {
                "title": "Documentar API com Swagger",
                "description": "Gerar documentação automática",
                "status": "cancelled",
                "priority": 4,
                "user_id": created_users[2].id,
                "category_id": created_categories[0].id,
            },
            {
                "title": "Refatorar models",
                "description": "Melhorar organização dos models",
                "status": "in_progress",
                "priority": 3,
                "user_id": created_users[1].id,
                "category_id": created_categories[0].id,
                "tags": "refactor,tech-debt",
            },
            {
                "title": "Configurar monitoramento",
                "description": "Prometheus + Grafana",
                "status": "pending",
                "priority": 4,
                "user_id": created_users[2].id,
                "category_id": created_categories[2].id,
                "due_date": now + timedelta(days=20),
            },
            {
                "title": "Melhorar validações de input",
                "description": "Usar marshmallow ou pydantic",
                "status": "pending",
                "priority": 3,
                "user_id": created_users[0].id,
                "category_id": created_categories[0].id,
                "tags": "improvement,validation",
            },
        ]

        for task_data in tasks_data:
            db.session.add(Task(**task_data))

        db.session.commit()
        logger.info("Seed concluído com sucesso!")
        logger.info("%s usuários", User.query.count())
        logger.info("%s categorias", Category.query.count())
        logger.info("%s tasks", Task.query.count())


if __name__ == "__main__":
    seed_data()
