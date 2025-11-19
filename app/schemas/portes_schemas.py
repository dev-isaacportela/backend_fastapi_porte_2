from pydantic import BaseModel, EmailStr, Field
from typing import List, Annotated


class PorteOut(BaseModel):
    id: Annotated[int, Field(description="ID do porte")]
    ano_emissao: Annotated[int, Field(description="Ano de emissão do porte")]
        #int | None = None
    mes_emissao: Annotated[int, Field(description="Mês de emissão do porte")]
    total: Annotated[int, Field(description="Total de portes emitidos")]

    uf: Annotated[str, Field(description="Unidade Federativa")]
    municipio: Annotated[str, Field(description="Município")]
    tipo: Annotated[str, Field(description="Tipo do porte")]
    status: Annotated[str, Field(description="Status do porte")]
    abrangencia: Annotated[str, Field(description="Abrangência do porte")]
    especie_arma: Annotated[str, Field(description="Espécie da arma")]
    marca_arma: Annotated[str, Field(description="Marca da arma")]
    calibre_arma: Annotated[str, Field(description="Calibre da arma")]
    sexo: Annotated[str, Field(description="Sexo do portador")]

    class Config:
        from_attributes = True
        json_encoders = {}
        
class PorteCreate(BaseModel):
    ano_emissao: Annotated[int, Field(description="Ano de emissão do porte")]
        #int | None = None
    mes_emissao: Annotated[int, Field(description="Mês de emissão do porte")]
    total: Annotated[int, Field(description="Total de portes emitidos")]

    uf_id: Annotated[int, Field(description="ID da Unidade Federativa")]
    municipio_id: Annotated[int, Field(description="ID do Município")]
    tipo_id: Annotated[int, Field(description="ID do Tipo do porte")]
    status_id: Annotated[int, Field(description="ID do Status do porte")]
    abrangencia_id: Annotated[int, Field(description="ID da Abrangência do porte")]
    especie_arma_id: Annotated[int, Field(description="ID da Espécie da arma")]
    marca_arma_id: Annotated[int, Field(description="ID da Marca da arma")]
    calibre_arma_id: Annotated[int, Field(description="ID do Calibre da arma")]
    sexo_id: Annotated[int, Field(description="ID do Sexo do portador")]

    class Config:
        from_attributes = True
        json_encoders = {}
        
class PorteUpdate(BaseModel):
    ano_emissao: Annotated[int, Field(description="Ano de emissão do porte")]
        #int | None = None
    mes_emissao: Annotated[int, Field(description="Mês de emissão do porte")]
    total: Annotated[int, Field(description="Total de portes emitidos")]

    uf_id: Annotated[int, Field(description="ID da Unidade Federativa")]
    municipio_id: Annotated[int, Field(description="ID do Município")]
    tipo_id: Annotated[int, Field(description="ID do Tipo do porte")]
    status_id: Annotated[int, Field(description="ID do Status do porte")]
    abrangencia_id: Annotated[int, Field(description="ID da Abrangência do porte")]
    especie_arma_id: Annotated[int, Field(description="ID da Espécie da arma")]
    marca_arma_id: Annotated[int, Field(description="ID da Marca da arma")]
    calibre_arma_id: Annotated[int, Field(description="ID do Calibre da arma")]
    sexo_id: Annotated[int, Field(description="ID do Sexo do portador")]

    class Config:
        from_attributes = True
        json_encoders = {}