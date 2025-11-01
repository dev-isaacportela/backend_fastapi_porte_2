from pydantic import BaseModel, EmailStr
from typing import List

# Esquema base para Usuário e autenticação

class UserBase(BaseModel):
    usuario_email: EmailStr
    
# 
class UserCreate(UserBase):
    usuario_nome: str
    usuario_sobrenome: str
    usuario_senha: str
    usuario_admin: bool = False
    
    class Config:
        from_attributes = True
        
class UserOut(UserBase):
    id: int
    usuario_nome: str
    usuario_sobrenome: str
    usuario_admin: bool

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    usuario_email: EmailStr | None = None
    
