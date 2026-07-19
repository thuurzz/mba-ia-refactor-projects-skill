from sqlalchemy import func

from src.errors import APIError
from src.extensions import db
from src.models.category import Category
from src.models.task import Task
from src.services.serialization_service import serialize_category
from src.services.validation_service import validate_category_payload


class CategoryController:
    @staticmethod
    def list_categories():
        counts = dict(
            db.session.query(Task.category_id, func.count(Task.id))
            .group_by(Task.category_id)
            .all()
        )
        return [
            serialize_category(category, counts.get(category.id, 0))
            for category in Category.list_all()
        ]

    @staticmethod
    def create_category(data):
        payload = validate_category_payload(data)
        category = Category(**payload)
        db.session.add(category)
        db.session.commit()
        return serialize_category(category), 201

    @staticmethod
    def update_category(category_id, data):
        category = Category.find_by_id(category_id)
        if not category:
            raise APIError("Categoria não encontrada", 404)
        payload = validate_category_payload(data, partial=True)
        for field, value in payload.items():
            setattr(category, field, value)
        db.session.commit()
        return serialize_category(category, len(category.tasks))

    @staticmethod
    def delete_category(category_id):
        category = Category.find_by_id(category_id)
        if not category:
            raise APIError("Categoria não encontrada", 404)
        for task in category.tasks:
            task.category = None
        db.session.delete(category)
        db.session.commit()
        return {"message": "Categoria deletada"}
