import os
from pathlib import Path

from dotenv import load_dotenv

# app/config.py → app/ → backend/ → raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Config:
    """Configuração base, lida a partir do ambiente."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-troque-em-producao")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Toda variável de ambiente é string: "a,b" precisa virar ["a", "b"]
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]


class TestConfig(Config):
    """Banco em memória: cada rodada de teste começa limpa."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
