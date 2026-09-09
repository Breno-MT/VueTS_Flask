from flask import Blueprint, request

from app.extensions import db
from app.models.task import Task

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@bp.get("")
def index():
    tasks = db.session.scalars(
        db.select(Task).order_by(Task.created_at.desc())
    ).all()
    return [task.to_dict() for task in tasks]


@bp.post("")
def store():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()

    if not title:
        return {"errors": {"title": "Campo obrigatório"}}, 422
    if len(title) > 200:
        return {"errors": {"title": "Máximo de 200 caracteres"}}, 422

    task = Task(title=title)
    db.session.add(task)
    db.session.commit()

    return task.to_dict(), 201


@bp.patch("/<int:task_id>")
def update(task_id: int):
    task = db.get_or_404(Task, task_id)
    data = request.get_json(silent=True) or {}

    if "done" in data:
        task.done = bool(data["done"])

    if "title" in data:
        title = (data["title"] or "").strip()
        if not title:
            return {"errors": {"title": "Campo obrigatório"}}, 422
        task.title = title

    db.session.commit()
    return task.to_dict()


@bp.delete("/<int:task_id>")
def destroy(task_id: int):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204
