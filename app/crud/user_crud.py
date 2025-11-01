from sqlalchemy.orm import Session
from app.models.orm import DBUser

def get_user_by_email(db: Session, email: str) -> DBUser | None:
    #busca o usuario pelo email
    return db.query(DBUser).filter(DBUser.usuario_email == email).first()

def get_user_by_id(db: Session, user_id: int) -> DBUser | None:
    #busca o usuario pelo id
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def get_all_users(db: Session) -> list[DBUser]:
    #busca todos os usuarios
    return db.query(DBUser).all()

def create_user(db: Session, usuario_nome: str, usuario_sobrenome: str, usuario_email: str, usuario_senha: str, usuario_admin: bool = False) -> DBUser:
    #cria um novo usuario
    db_user = DBUser(
        usuario_nome=usuario_nome,
        usuario_sobrenome=usuario_sobrenome,
        usuario_email=usuario_email,
        usuario_senha=usuario_senha,
        usuario_admin=usuario_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user