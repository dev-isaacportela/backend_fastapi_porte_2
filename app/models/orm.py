from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# Modelos de busca para tabelas relacionadas

class DBAbrangencia(Base):
    __tablename__ = "ABRANGENCIA"
    id = Column(Integer, primary_key=True, index=True)
    abrangencia_nome = Column(String, unique=True, nullable=False)

class DBCalibre(Base):
    __tablename__ = "CALIBRE_ARMA"
    id = Column(Integer, primary_key=True, index=True)
    calibre_nome = Column(String, unique=True, nullable=False)

class DBMarca(Base):
    __tablename__ = "MARCA_ARMA"
    id = Column(Integer, primary_key=True, index=True)
    marca_nome = Column(String, unique=True, nullable=False)

class DBEspecie(Base):
    __tablename__ = "ESPECIE_ARMA"
    id = Column(Integer, primary_key=True, index=True)
    especie_nome = Column(String, unique=True, nullable=False)

class DBTipo(Base):
    __tablename__ = "TIPO"
    id = Column(Integer, primary_key=True, index=True)
    tipo_nome = Column(String, unique=True, nullable=False)

class DBStatus(Base):
    __tablename__ = "STATUS"
    id = Column(Integer, primary_key=True, index=True)
    status_nome = Column(String, unique=True, nullable=False)

class DBMunicipio(Base):
    __tablename__ = "MUNICIPIO"
    id = Column(Integer, primary_key=True, index=True)
    municipio_nome = Column(String, unique=True, nullable=False)

class DBUF(Base):
    __tablename__ = "UF"
    id = Column(Integer, primary_key=True, index=True)
    uf_nome = Column(String, unique=True, nullable=False)

class DBSexo(Base):
    __tablename__ = "SEXO"
    id = Column(Integer, primary_key=True, index=True)
    sexo_nome = Column(String, unique=True, nullable=False)

#Modelo de Usuários

class DBUser(Base):
    __tablename__ = "USUARIOS"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_nome = Column(String, index=True, nullable=False)
    usuario_sobrenome = Column(String, nullable=False)
    usuario_email = Column(String, unique=True, index=True, nullable=False)
    usuario_senha = Column(String, nullable=False)
    usuario_admin = Column(Boolean, default=False, nullable=False)
    
#Modelo Principal
class DBPortes(Base):
    __tablename__ = "PORTES" 
    
    id = Column(Integer, primary_key=True, index=True)
    ano_emissao = Column(Integer)
    mes_emissao = Column(Integer)
    total = Column(Integer)
    
    # FKS
    uf_id = Column(Integer, ForeignKey("UF.id"))
    municipio_id = Column(Integer, ForeignKey("MUNICIPIO.id"))
    tipo_id = Column(Integer, ForeignKey("TIPO.id"))
    status_id = Column(Integer, ForeignKey("STATUS.id"))
    abrangencia_id = Column(Integer, ForeignKey("ABRANGENCIA.id"))
    especie_arma_id = Column(Integer, ForeignKey("ESPECIE_ARMA.id"))
    marca_arma_id = Column(Integer, ForeignKey("MARCA_ARMA.id"))
    calibre_arma_id = Column(Integer, ForeignKey("CALIBRE_ARMA.id"))
    sexo_id = Column(Integer, ForeignKey("SEXO.id"))
    
    # Relacionamentos
    uf = relationship("DBUF")
    municipio = relationship("DBMunicipio")
    tipo = relationship("DBTipo")
    status = relationship("DBStatus")
    abrangencia = relationship("DBAbrangencia")
    especie_arma = relationship("DBEspecie")
    marca_arma = relationship("DBMarca")
    calibre_arma = relationship("DBCalibre")
    sexo = relationship("DBSexo")