from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa do SQLAlchemy 2.0.

    Passar uma Base própria (em vez de deixar o Flask-SQLAlchemy criar a dele)
    é o que habilita a tipagem moderna com Mapped[] nos models.
    """


db = SQLAlchemy(model_class=Base)
