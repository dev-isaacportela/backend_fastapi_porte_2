from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud import user_crud
from app.core.security import get_current_user, get_current_active_admin
from app.models.orm import DBUser
from app.schemas.user_schemas import UserCreate, UserOut

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Registro de novo usuário")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.usuario_email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    
    return user_crud.create_new_user(db, user=user)

@router.get("/me", response_model=UserOut, summary="Obter dados do usuário logado")
def read_users_me(current_user: DBUser = Depends(get_current_user)):

    return current_user

@router.get("/", response_model=list[UserOut], summary="Listar todos os usuários (Admin Required)")
def read_all_users(
    db: Session = Depends(get_db), 
    current_admin: DBUser = Depends(get_current_active_admin) 
):

    users = user_crud.get_all_users(db)
    return users