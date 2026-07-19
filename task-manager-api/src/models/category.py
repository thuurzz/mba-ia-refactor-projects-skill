from datetime import UTC, datetime

from src.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    color = db.Column(db.String(7), default="#000000", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    tasks = db.relationship("Task", back_populates="category", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def find_by_id(cls, category_id):
        return db.session.get(cls, category_id)

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.name.asc()).all()
