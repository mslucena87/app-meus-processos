from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PrazoSchema(BaseModel):
    id: int
    processo_id: int
    descricao: str
    data_inicio: date
    data_fatal: date
    dias_uteis: int
    status: str

    class Config:
        from_attributes = True

class ProcessoSchema(BaseModel):
    id: int
    numero_cnj: str
    tribunal: str
    classe: Optional[str] = None
    orgao_julgador: Optional[str] = None
    prazos: List[PrazoSchema] = []

    class Config:
        from_attributes = True

class SincronizarOABRequest(BaseModel):
    oab_numero: str
    oab_uf: str
    tribunal: str = "tjsp"

class DashboardStatsSchema(BaseModel):
    total_processos: int
    prazos_pendentes: int
    prazos_urgentes: int