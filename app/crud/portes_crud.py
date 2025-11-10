from sqlalchemy.orm import Session, joinedload
from sqlalchemy import outerjoin
from app.core.security import get_password_hash
from app.models.orm import (
    DBPortes,
    DBUF,
    DBMunicipio,
    DBTipo,
    DBStatus,
    DBAbrangencia,
    DBEspecie,
    DBMarca,
    DBCalibre,
    DBSexo,
)
from typing import Optional

def get_all_portes(db: Session) -> list[dict]:
    portes = (
        db.query(DBPortes)
        .options(
            joinedload(DBPortes.uf),
            joinedload(DBPortes.municipio),
            joinedload(DBPortes.tipo),
            joinedload(DBPortes.status),
            joinedload(DBPortes.abrangencia),
            joinedload(DBPortes.especie_arma),
            joinedload(DBPortes.marca_arma),
            joinedload(DBPortes.calibre_arma),
            joinedload(DBPortes.sexo),
        )
        .all()
    )

    result = []
    for p in portes:
        result.append({
            "id": p.id,
            "ano_emissao": p.ano_emissao,
            "mes_emissao": p.mes_emissao,
            "total": p.total,
            "uf": p.uf.uf_nome if p.uf else None,
            "municipio": p.municipio.municipio_nome if p.municipio else None,
            "tipo": p.tipo.tipo_nome if p.tipo else None,
            "status": p.status.status_nome if p.status else None,
            "abrangencia": p.abrangencia.abrangencia_nome if p.abrangencia else None,
            "especie_arma": p.especie_arma.especie_nome if p.especie_arma else None,
            "marca_arma": p.marca_arma.marca_nome if p.marca_arma else None,
            "calibre_arma": p.calibre_arma.calibre_nome if p.calibre_arma else None,
            "sexo": p.sexo.sexo_nome if p.sexo else None,
        })

    return result


def get_porte_by_id(db: Session, porte_id: int) -> Optional[dict]:
    p = (
        db.query(DBPortes)
        .options(
            joinedload(DBPortes.uf),
            joinedload(DBPortes.municipio),
            joinedload(DBPortes.tipo),
            joinedload(DBPortes.status),
            joinedload(DBPortes.abrangencia),
            joinedload(DBPortes.especie_arma),
            joinedload(DBPortes.marca_arma),
            joinedload(DBPortes.calibre_arma),
            joinedload(DBPortes.sexo),
        )
        .filter(DBPortes.id == porte_id)
        .first()
    )

    if not p:
        return None

    return {
        "id": p.id,
        "ano_emissao": p.ano_emissao,
        "mes_emissao": p.mes_emissao,
        "total": p.total,
        "uf": p.uf.uf_nome if p.uf else None,
        "municipio": p.municipio.municipio_nome if p.municipio else None,
        "tipo": p.tipo.tipo_nome if p.tipo else None,
        "status": p.status.status_nome if p.status else None,
        "abrangencia": p.abrangencia.abrangencia_nome if p.abrangencia else None,
        "especie_arma": p.especie_arma.especie_nome if p.especie_arma else None,
        "marca_arma": p.marca_arma.marca_nome if p.marca_arma else None,
        "calibre_arma": p.calibre_arma.calibre_nome if p.calibre_arma else None,
        "sexo": p.sexo.sexo_nome if p.sexo else None,
    }