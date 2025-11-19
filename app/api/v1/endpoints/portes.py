from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import portes_crud
from app.db import get_db, verify_token
from typing import Annotated
from pydantic import Field
from app.models.orm import DBUser
from app.schemas import PorteCreate


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
    return portes

@portes_router.get("/{porte_id}", summary="Porte por ID", status_code=status.HTTP_200_OK)
def get_porte_by_id(
    porte_id: Annotated[int, Field(description="ID do porte a ser obtido")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
):
    
    porte = portes_crud.get_porte_by_id(db, porte_id)
    if not porte:
        raise HTTPException(status_code=404, detail="Porte não encontrado")
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    return porte

#@portes_router.get("/status/{status_nome}", summary="Portes por Status", status_code=status.HTTP_200_OK)
#@portes_router.get("/uf/{uf_nome}", summary="Portes por Uf", status_code=status.HTTP_200_OK)
#@portes_router.get("/municipio/{municipio_nome}", summary="Portes por Municipio", status_code=status.HTTP_200_OK)
#@portes_router.get("/filtros/", summary="Portes com múltiplos filtros", status_code=status.HTTP_200_OK)

@portes_router.post("/create_porte", response_model=PorteCreate, summary="Criação de um novo porte", status_code=status.HTTP_201_CREATED)
def create_porte(
    porte_data: Annotated[PorteCreate, Field(description="Dados do porte a ser criado")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
):
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    new_porte = portes_crud.create_porte(db, porte_data.model_dump())
    return new_porte

@portes_router.put("/update_porte/{porte_id}", summary="Atualização de um porte existente", status_code=status.HTTP_200_OK)
def update_porte(
    porte_id: Annotated[int, Field(description="ID do porte a ser atualizado")],
    porte_data: Annotated[PorteCreate, Field(description="Dados atualizados do porte")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
):
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    updated_porte = portes_crud.update_porte(db, porte_id, porte_data.model_dump())
    if not updated_porte:
        raise HTTPException(status_code=404, detail="Porte não encontrado para atualização")
    return updated_porte

@portes_router.delete("/delete_porte/{porte_id}", summary="Exclusão de um porte", status_code=status.HTTP_200_OK)
def delete_porte(
    porte_id: Annotated[int, Field(description="ID do porte a ser excluído")],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[DBUser, Depends(verify_token)]
):
    if not user.usuario_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    deleted_porte = portes_crud.delete_porte(db, porte_id)
    if not deleted_porte:
        raise HTTPException(status_code=404, detail="Porte não encontrado para exclusão")
    return {"detail": "Porte excluído com sucesso"}