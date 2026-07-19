from datetime import timedelta

from sqlalchemy import case, func

from src.errors import APIError
from src.extensions import db
from src.models.category import Category
from src.models.task import Task
from src.models.user import User
from src.services.datetime_service import ensure_utc, utc_now


class ReportController:
    @staticmethod
    def summary_report():
        now = utc_now()
        seven_days_ago = now - timedelta(days=7)

        total_tasks = db.session.query(func.count(Task.id)).scalar() or 0
        total_users = db.session.query(func.count(User.id)).scalar() or 0
        total_categories = db.session.query(func.count(Category.id)).scalar() or 0

        status_counts = dict(db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all())
        priority_counts = dict(db.session.query(Task.priority, func.count(Task.id)).group_by(Task.priority).all())

        overdue_tasks = [
            task
            for task in Task.list_all()
            if task.due_date
            and ensure_utc(task.due_date) < now
            and task.status not in {"done", "cancelled"}
        ]

        user_productivity_rows = (
            db.session.query(
                User.id,
                User.name,
                func.count(Task.id),
                func.coalesce(func.sum(case((Task.status == "done", 1), else_=0)), 0),
            )
            .outerjoin(Task, Task.user_id == User.id)
            .group_by(User.id, User.name)
            .all()
        )

        recent_tasks = db.session.query(func.count(Task.id)).filter(Task.created_at >= seven_days_ago).scalar() or 0
        recent_done = (
            db.session.query(func.count(Task.id))
            .filter(Task.status == "done", Task.updated_at >= seven_days_ago)
            .scalar()
            or 0
        )

        return {
            "generated_at": now.isoformat(),
            "overview": {
                "total_tasks": total_tasks,
                "total_users": total_users,
                "total_categories": total_categories,
            },
            "tasks_by_status": {
                "pending": status_counts.get("pending", 0),
                "in_progress": status_counts.get("in_progress", 0),
                "done": status_counts.get("done", 0),
                "cancelled": status_counts.get("cancelled", 0),
            },
            "tasks_by_priority": {
                "critical": priority_counts.get(1, 0),
                "high": priority_counts.get(2, 0),
                "medium": priority_counts.get(3, 0),
                "low": priority_counts.get(4, 0),
                "minimal": priority_counts.get(5, 0),
            },
            "overdue": {
                "count": len(overdue_tasks),
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "days_overdue": (now - ensure_utc(task.due_date)).days,
                    }
                    for task in overdue_tasks
                ],
            },
            "recent_activity": {
                "tasks_created_last_7_days": recent_tasks,
                "tasks_completed_last_7_days": recent_done,
            },
            "user_productivity": [
                {
                    "user_id": user_id,
                    "user_name": user_name,
                    "total_tasks": total,
                    "completed_tasks": completed,
                    "completion_rate": round((completed / total) * 100, 2) if total else 0,
                }
                for user_id, user_name, total, completed in user_productivity_rows
            ],
        }

    @staticmethod
    def user_report(user_id):
        user = User.find_by_id(user_id)
        if not user:
            raise APIError("Usuário não encontrado", 404)

        now = utc_now()
        total = len(user.tasks)
        done = sum(1 for task in user.tasks if task.status == "done")
        pending = sum(1 for task in user.tasks if task.status == "pending")
        in_progress = sum(1 for task in user.tasks if task.status == "in_progress")
        cancelled = sum(1 for task in user.tasks if task.status == "cancelled")
        overdue = sum(
            1
            for task in user.tasks
            if task.due_date
            and ensure_utc(task.due_date) < now
            and task.status not in {"done", "cancelled"}
        )
        high_priority = sum(1 for task in user.tasks if task.priority <= 2)

        return {
            "user": user.to_dict(),
            "statistics": {
                "total_tasks": total,
                "done": done,
                "pending": pending,
                "in_progress": in_progress,
                "cancelled": cancelled,
                "overdue": overdue,
                "high_priority": high_priority,
                "completion_rate": round((done / total) * 100, 2) if total else 0,
            },
        }
