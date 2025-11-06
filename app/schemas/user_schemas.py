<<<<<<< HEAD
from pydantic import BaseModel, EmailStr, Field
from typing import List, Annotated
=======
from pydantic import BaseModel, EmailStr
from typing import List
>>>>>>> 76d042f830440c089a3dcf227d1245534ad2ff22

# Esquema base para Usuário e autenticação

class UserBase(BaseModel):
    usuario_email: EmailStr
    
# 
class UserCreate(UserBase):
<<<<<<< HEAD
    usuario_nome: Annotated[str, Field(max_length=35, min_length=3, description="Nome do usuário, entre 3 e 35 caracteres")]
    usuario_sobrenome: Annotated[str, Field(max_length=40, min_length=3, description="Sobrenome do usuário, entre 3 e 40 caracteres")]
    usuario_senha: str
    usuario_admin: Annotated[bool, Field(default=False, description="Define se o usuário é admin ou não")]
    
=======
    usuario_nome: str
    usuario_sobrenome: str
    usuario_senha: str
    usuario_admin: bool = False
>>>>>>> 76d042f830440c089a3dcf227d1245534ad2ff22
    
class UserLogin(UserBase):
    usuario_email: EmailStr
    usuario_senha: str
        
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
    
    
