from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt

from app.db.database import get_db
from app.crud.user_crud import get_user_by_email
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.schemas.user_schemas import Token, UserOut

from app.crud import user_crud
from app.schemas.user_schemas import UserCreate, UserOut

router = APIRouter()

def criar_token(id_usuario):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": id_usuario, "exp": access_token_expires}
    jwt_codificado = jwt.ecode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

@router.post("/create_user", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Registro de novo usuário")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.usuario_email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    
    return user_crud.create_new_user(db, user=user)

