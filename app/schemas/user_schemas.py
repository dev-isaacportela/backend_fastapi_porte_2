from pydantic import BaseModel, EmailStr, Field
from typing import List, Annotated

# Esquema base para Usuário e autenticação

class UserBase(BaseModel):
    usuario_email: EmailStr
    
# 
class UserCreate(UserBase):
    usuario_nome: Annotated[str, Field(max_length=35, min_length=3, description="Nome do usuário, entre 3 e 35 caracteres")]
    usuario_sobrenome: Annotated[str, Field(max_length=40, min_length=3, description="Sobrenome do usuário, entre 3 e 40 caracteres")]
    usuario_senha: str
    usuario_admin: Annotated[bool, Field(default=False, description="Define se o usuário é admin ou não")]
    
    
class UserLogin(UserBase):
    usuario_email: Annotated[EmailStr, Field(description="Email do usuário para login")]
    usuario_senha: Annotated[str, Field(description="Senha do usuário para login")]
        
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
    
    
