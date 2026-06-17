"""Database helper: build a SQLAlchemy engine from environment variables.

Credentials are read from the environment so they never live in source control.
Copy `.env.example` to `.env`, fill in your values, and they will be loaded
automatically (via python-dotenv) when these scripts run.

Required:  DB_USER, DB_PASS, DB_NAME
Optional:  DB_HOST (default localhost), DB_PORT (default 5432)
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

try:
    # Optional: load a local .env file if python-dotenv is installed.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def get_engine() -> Engine:
    """Return a SQLAlchemy engine for the crypto warehouse.

    Raises a clear, actionable error if required credentials are missing
    instead of failing deep inside SQLAlchemy with a cryptic message.
    """
    try:
        user = os.environ["DB_USER"]
        password = os.environ["DB_PASS"]
        name = os.environ["DB_NAME"]
    except KeyError as missing:
        raise SystemExit(
            f"Missing required environment variable: {missing}.\n"
            "Copy .env.example to .env and set your database credentials."
        )

    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")

    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    )
