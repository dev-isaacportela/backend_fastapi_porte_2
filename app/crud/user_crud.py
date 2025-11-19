from sqlalchemy.orm import Session
from app.models.orm import DBUser
from app.core.security import get_password_hash
from fastapi import HTTPException, status

from app.schemas.user_schemas import UserCreate


def get_user_by_email(db: Session, email: str) -> DBUser | None:
    #busca o usuario pelo email
    return db.query(DBUser).filter(DBUser.usuario_email == email).first()

def get_user_by_id(db: Session, user_id: int) -> DBUser | None:
    #busca o usuario pelo id
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def get_all_users(db: Session) -> list[DBUser]:
    #busca todos os usuarios
    return db.query(DBUser).all()

def create_new_user(db: Session, user: UserCreate) -> DBUser:
    #cria um novo usuario
    hashed_password = get_password_hash(user.usuario_senha)
    
    db_user = DBUser(
        usuario_nome=user.usuario_nome,
        usuario_sobrenome=user.usuario_sobrenome,
        usuario_email=user.usuario_email,
        usuario_senha=hashed_password,
        usuario_admin=user.usuario_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: dict) -> DBUser | None:
    #atualiza um usuario existente
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    new_email = user_data.get("usuario_email")
    
    if new_email and new_email != db_user.usuario_email:
        # Verifica se existe OUTRO usuário com esse mesmo e-mail
        email_exists = db.query(DBUser).filter(DBUser.usuario_email == new_email).first()
        
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está sendo usado por outro usuário."
            )
    
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    #deleta um usuario
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def auth_user(db: Session, email: str, password: str) -> DBUser | None:
    #autentica o usuario
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user

def get_admin_users(db: Session) -> list[DBUser]:
    #busca todos os usuarios administradores
    return db.query(DBUser).filter(DBUser.usuario_admin == True).all()

def change_user_password(db: Session, user_id: int, new_password: str) -> DBUser | None:
    #atualiza a senha do usuario
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    hashed_password = get_password_hash(new_password)
    db_user.usuario_senha = hashed_password

    db.commit()
    db.refresh(db_user)
    return db_user