from sqlalchemy.orm import Session
from app.models.orm import DBUser

from app.schemas.user_schemas import UserCreate
from app.core.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> DBUser | None:
    #busca o usuario pelo email
    return db.query(DBUser).filter(DBUser.usuario_email == email).first()

def get_user_by_id(db: Session, user_id: int) -> DBUser | None:
    #busca o usuario pelo id
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def get_all_users(db: Session) -> list[DBUser]:
    #busca todos os usuarios
    return db.query(DBUser).all()

def create_user(db: Session, user: UserCreate) -> DBUser:
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