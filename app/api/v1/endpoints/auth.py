from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from jose import jwt
from app.db import get_db, verify_token
from app.core import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_scheme, verify_password
from app.crud import user_crud
from app.schemas import UserCreate, UserLogin, UserOut
from app.models.orm import DBUser
from typing import Annotated

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_token(usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    access_token_expires = datetime.now(timezone.utc) + duracao_token
    dic_info = { "sub": str(usuario_id), "exp": int(access_token_expires.timestamp())}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def auth_user(
    email: Annotated[str, Body()],
    senha: Annotated[str, Body()],
    db: Annotated[Session, Depends(get_db)]
    ):
    
    user = db.query(DBUser).filter(DBUser.usuario_email == email).first()
    if not user:
        return False
    elif not verify_password(senha, user.usuario_senha):
        return False
    return user
        
@auth_router.get("/refresh")
async def use_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)], 
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    access_token = create_token(user.id)
    return {"access_token": access_token,
            "token_type": "bearer"}
    
@auth_router.post("/login")
async def login(
    login_schema: Annotated[UserLogin, Body()],
    db: Annotated[Session, Depends(get_db)]
    ):
    
    usuario = auth_user(login_schema.usuario_email, login_schema.usuario_senha, db)
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")

    else:
        access_token = create_token(usuario_id=usuario.id)
        return {"access_token": access_token,
                "token_type": "bearer"}
        
@auth_router.post("/login-form")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Annotated[Session, Depends(get_db)]
    ):
    
    usuario = auth_user(form_data.username, form_data.password, db)
    #usuario = db.query(DBUser).filter(DBUser.username == login_schema.usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")

    else:
        access_token = create_token(usuario_id=usuario.id)
        return {"access_token": access_token,
                "token_type": "bearer"}