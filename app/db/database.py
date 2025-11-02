from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.base import Base
from app.models.orm import DBUser
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme

SQLALCHEMY_DATABASE_URL = "sqlite:///./banco.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
#ter acesso ao banco de dados
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def verify_token(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError:
        return HTTPException(status_code=401, detail="Acesso negado, verifique a válidade do token")
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    
    if not user:
        return HTTPException(status_code=401, detail="Acesso inválido")
    return user