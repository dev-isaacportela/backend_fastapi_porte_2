from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./banco.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependência para obter a sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()