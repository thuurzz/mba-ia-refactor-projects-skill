from datetime import UTC, datetime

from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from src.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="pending", nullable=False)
    priority = db.Column(db.Integer, default=3, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    due_date = db.Column(db.DateTime(timezone=True), nullable=True)
    tags = db.Column(db.String(500), nullable=True)

    user = db.relationship("User", back_populates="tasks", lazy="selectin")
    category = db.relationship("Category", back_populates="tasks", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags.split(",") if self.tags else [],
        }

    @classmethod
    def find_by_id(cls, task_id):
        return db.session.get(cls, task_id)

    @classmethod
    def list_all(cls):
        return cls.query.options(selectinload(cls.user), selectinload(cls.category)).order_by(cls.id.asc()).all()

    @classmethod
    def search(cls, query_text=None, status=None, priority=None, user_id=None):
        query = cls.query.options(selectinload(cls.user), selectinload(cls.category))
        if query_text:
            search_term = f"%{query_text}%"
            query = query.filter(or_(cls.title.ilike(search_term), cls.description.ilike(search_term)))
        if status:
            query = query.filter(cls.status == status)
        if priority is not None:
            query = query.filter(cls.priority == priority)
        if user_id is not None:
            query = query.filter(cls.user_id == user_id)
        return query.order_by(cls.id.asc()).all()
