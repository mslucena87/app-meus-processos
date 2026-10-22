from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)

class Processo(Base):
    __tablename__ = "processos"

    id = Column(Integer, primary_key=True, index=True)
    numero_cnj = Column(String(25), unique=True, index=True, nullable=False)
    tribunal = Column(String(20), nullable=False)
    classe = Column(String(150))
    orgao_julgador = Column(String(200))
    resumo_ia = Column(Text, nullable=True)

    prazos = relationship("Prazo", back_populates="processo", cascade="all, delete-orphan")

class Prazo(Base):
    __tablename__ = "prazos"

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    descricao = Column(String(255), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fatal = Column(Date, nullable=False, index=True)
    dias_uteis = Column(Integer, nullable=False)
    status = Column(String(20), default="PENDENTE")

    processo = relationship("Processo", back_populates="prazos")