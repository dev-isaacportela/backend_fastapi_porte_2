from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import portes_crud
from app.db import get_db, verify_token
from typing import Annotated
from pydantic import Field
from app.models.orm import DBUser

portes_router = APIRouter(prefix="/portes", tags=["Portes"], dependencies=[Depends(verify_token)])

@portes_router.get("/", summary="Listagem de todos os portes", status_code=status.HTTP_200_OK)
def list_all_portes(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
):
    
    portes = portes_crud.get_all_portes(db)
    if not portes:
        raise HTTPException(status_code=404, detail="Nenhum porte encontrado")
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")

@portes_router.get("/{porte_id}", summary="Porte por ID", status_code=status.HTTP_200_OK)
def get_porte_by_id(
    porte_id: Annotated[int, Field(description="ID do porte a ser obtido")],
    db: Annotated[Session, Depends(get_db)]
):
    
    porte = portes_crud.get_porte_by_id(db, porte_id)
    if not porte:
        raise HTTPException(status_code=404, detail="Porte não encontrado")
    return porte
