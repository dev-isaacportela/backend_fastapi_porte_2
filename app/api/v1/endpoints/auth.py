from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from jose import jwt
from app.db.database import get_db, verify_token
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_scheme, verify_password
from app.schemas.user_schemas import UserOut
from app.crud import user_crud
from app.schemas.user_schemas import UserCreate, UserLogin
from app.models.orm import DBUser
from typing import Annotated

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_token(usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    access_token_expires = datetime.now(timezone.utc) + duracao_token
    dic_info = { "sub": str(usuario_id), "exp": int(access_token_expires.timestamp())}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def auth_user(email: str, senha: str, db: Session):
    user = db.query(DBUser).filter(DBUser.usuario_email == email).first()
    if not user:
        return False
    elif not verify_password(senha, user.usuario_senha):
        return False
    return user

@auth_router.post("/create_user", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Registro de novo usuário")
def register_user(
    user: Annotated[UserCreate, Body()], 
    db: Annotated[Session, Depends(get_db)] 
    #boa prática para tipar dependências
    ):
    
    db_user = user_crud.get_user_by_email(db, email=user.usuario_email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    
    return user_crud.create_new_user(db, user=user)

@auth_router.post("/login")
async def login(login_schema: UserLogin, db: Session = Depends(get_db)):
    usuario = auth_user(login_schema.usuario_email, login_schema.usuario_senha, db)
    #usuario = db.query(DBUser).filter(DBUser.username == login_schema.usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")

    else:
        access_token = create_token(usuario_id=usuario.id)
        return {"access_token": access_token,
                "token_type": "bearer"}
        
@auth_router.post("/login-form")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = auth_user(form_data.username, form_data.password, db)
    #usuario = db.query(DBUser).filter(DBUser.username == login_schema.usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")

    else:
        access_token = create_token(usuario_id=usuario.id)
        return {"access_token": access_token,
                "token_type": "bearer"}
        
@auth_router.get("/refresh")
async def use_refresh_token(token: str = Depends(oauth2_scheme), user: DBUser = Depends(verify_token)):
    access_token = create_token(user.id)
    return {"access_token": access_token,
            "token_type": "bearer"}