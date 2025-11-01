from pydantic import BaseModel, EmailStr
from typing import List


class PorteOut(BaseModel):
    id: int
    ano_emissao: int | None = None
    mes_emissao: int | None = None
    total: int | None = None

    uf: str | None = None
    municipio: str | None = None
    tipo: str | None = None
    status: str | None = None
    abrangencia: str | None = None
    especie_arma: str | None = None
    marca_arma: str | None = None
    calibre_arma: str | None = None
    sexo: str | None = None

    class Config:
        from_attributes = True
        json_encoders = {}