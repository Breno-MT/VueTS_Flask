from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db


def create_app(config_object: type[Config] = Config) -> Flask:
    """Application factory: monta e devolve uma instância configurada."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # Fase 2 do padrão de duas fases: vincular as extensões a ESTE app
    db.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Rotas do sistema
    from app.routes.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    with app.app_context():
        from app import models  # noqa: F401 — registra Task nos metadados

        db.create_all()

    return app
