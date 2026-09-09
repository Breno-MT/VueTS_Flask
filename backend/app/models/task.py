from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

BRASILIA_TZ = timezone(timedelta(hours=-3))


class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(BRASILIA_TZ),
    )

    def to_dict(self) -> dict:
        """Converte para o formato que o frontend espera (camelCase)."""
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "createdAt": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Task {self.id} {self.title!r}>"
