from sqlalchemy import func

from src.constants import VALID_STATUSES
from src.errors import APIError
from src.extensions import db
from src.models.category import Category
from src.models.task import Task
from src.models.user import User
from src.services.datetime_service import ensure_utc, utc_now
from src.services.serialization_service import serialize_task
from src.services.validation_service import validate_task_payload


class TaskController:
    @staticmethod
    def list_tasks():
        return [serialize_task(task) for task in Task.list_all()]

    @staticmethod
    def get_task(task_id):
        task = Task.find_by_id(task_id)
        if not task:
            raise APIError("Task não encontrada", 404)
        return serialize_task(task)

    @staticmethod
    def create_task(data):
        payload = validate_task_payload(data)
        TaskController._validate_relations(payload)

        task = Task(**payload)
        db.session.add(task)
        db.session.commit()
        return serialize_task(task), 201

    @staticmethod
    def update_task(task_id, data):
        task = Task.find_by_id(task_id)
        if not task:
            raise APIError("Task não encontrada", 404)

        payload = validate_task_payload(data, partial=True)
        TaskController._validate_relations(payload)
        for field, value in payload.items():
            setattr(task, field, value)
        task.updated_at = utc_now()
        db.session.commit()
        return serialize_task(task)

    @staticmethod
    def delete_task(task_id):
        task = Task.find_by_id(task_id)
        if not task:
            raise APIError("Task não encontrada", 404)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deletada com sucesso"}

    @staticmethod
    def search_tasks(filters):
        status = filters.get("status") or None
        priority = filters.get("priority")
        user_id = filters.get("user_id")
        if status and status not in VALID_STATUSES:
            raise APIError("Status inválido", 400)
        try:
            parsed_priority = int(priority) if priority not in (None, "") else None
            parsed_user_id = int(user_id) if user_id not in (None, "") else None
        except ValueError as exc:
            raise APIError("Filtro numérico inválido", 400) from exc

        tasks = Task.search(
            query_text=(filters.get("q") or "").strip() or None,
            status=status,
            priority=parsed_priority,
            user_id=parsed_user_id,
        )
        return [serialize_task(task) for task in tasks]

    @staticmethod
    def task_stats():
        counts = dict(
            db.session.query(Task.status, func.count(Task.id))
            .group_by(Task.status)
            .all()
        )
        total = db.session.query(func.count(Task.id)).scalar() or 0
        overdue = sum(
            1
            for task in Task.list_all()
            if task.due_date
            and ensure_utc(task.due_date) < utc_now()
            and task.status not in {"done", "cancelled"}
        )
        done = counts.get("done", 0)
        return {
            "total": total,
            "pending": counts.get("pending", 0),
            "in_progress": counts.get("in_progress", 0),
            "done": done,
            "cancelled": counts.get("cancelled", 0),
            "overdue": overdue,
            "completion_rate": round((done / total) * 100, 2) if total else 0,
        }

    @staticmethod
    def _validate_relations(payload):
        user_id = payload.get("user_id")
        category_id = payload.get("category_id")
        if user_id is not None and user_id != "" and not User.find_by_id(user_id):
            raise APIError("Usuário não encontrado", 404)
        if category_id is not None and category_id != "" and not Category.find_by_id(category_id):
            raise APIError("Categoria não encontrada", 404)
