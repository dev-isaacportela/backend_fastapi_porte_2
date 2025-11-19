from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from jose import jwt
from app.db import get_db, verify_token
from app.core import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_scheme, verify_password
from app.crud import user_crud
from app.schemas import UserCreate, UserLogin, UserOut, UserPasswordChange
from app.models.orm import DBUser
from typing import Annotated

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get("/user/{user_email}", response_model=UserOut, status_code=status.HTTP_200_OK, summary="Obter dados do usuário pelo e-mail")
async def get_user_by_email_route(
    user_email: Annotated[str, Path(..., description="E-mail do usuário")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    user = user_crud.get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    return user

@user_router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK, summary="Obter dados do usuário autenticado")
async def get_current_user_route(
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    return user

@user_router.get("/all_users", response_model=list[UserOut], status_code=status.HTTP_200_OK, summary="Obter todos os usuários")
async def get_all_users_route(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    users = user_crud.get_all_users(db)
    return users

@user_router.get("/is_admin", status_code=status.HTTP_200_OK, summary="Verificar se o usuário autenticado é administrador")
async def is_admin_route(
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    return {"is_admin": user.usuario_admin}

@user_router.post("/create_user", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Registro de novo usuário")
def register_user(
    user: Annotated[UserCreate, Body()], 
    db: Annotated[Session, Depends(get_db)] 
    #boa prática para tipar dependências
    ):
    
    db_user = user_crud.get_user_by_email(db, email=user.usuario_email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    
    return user_crud.create_new_user(db, user=user)

@user_router.put("/update_user/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK, summary="Atualizar dados do usuário")
async def update_user_route(
    user_id: Annotated[int, Path(..., description="ID do usuário a ser atualizado")],
    user_data: Annotated[UserCreate, Body()],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    if not user.usuario_admin and user.id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    updated_user = user_crud.update_user(db, user_id, user_data.model_dump())
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para atualização")
    return updated_user

@user_router.put("/change_password/{user_id}", status_code=status.HTTP_200_OK, summary="Alterar a senha do usuário")
async def change_password_route(
    user_id: Annotated[int, Path(..., description="ID do usuário que terá a senha alterada")],
    new_password: Annotated[UserPasswordChange, Body(..., description="Nova senha do usuário")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    if not user.usuario_admin and user.id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    
    updated_user = user_crud.change_user_password(db, user_id, new_password)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para alteração de senha")
    
    return {"detail": "Senha alterada com sucesso"}

@user_router.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK, summary="Excluir um usuário")
async def delete_user_route(
    user_id: Annotated[int, Path(..., description="ID do usuário a ser excluído")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
    ):
    
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    deleted = user_crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão")
    return {"detail": "Usuário excluído com sucesso"}