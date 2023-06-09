import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

db_file = os.environ.get("KNOWLEDGE_DB_FILE", default="live.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///" + db_file

# SQLALCHEMY_DATABASE_URL = "sqlite:///./web_apps.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, echo=True
)

LocalSession: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
