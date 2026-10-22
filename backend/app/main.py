from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date, timedelta
import jwt
from passlib.context import CryptContext

from .database import engine, Base, get_db
from .models import Processo, Prazo, Usuario
from .schemas import SincronizarOABRequest, DashboardStatsSchema, PrazoSchema, LoginRequest, TokenResponse
from .datajud import DataJudClient
from .ai import LegalAIService

SECRET_KEY = "sua-chave-secreta-super-segura-aqui"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LegalOps API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria um usuário padrão no startup se não existir (ex: admin@legalops.com / senha123)
@app.on_event("startup")
def criar_usuario_padrao():
    db = next(get_db())
    admin = db.query(Usuario).filter(Usuario.email == "admin@legalops.com").first()
    if not admin:
        senha_hash = pwd_context.hash("senha123")
        novo_admin = Usuario(email="admin@legalops.com", senha_hash=senha_hash)
        db.add(novo_admin)
        db.commit()
    db.close()

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/api/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == req.email).first()
    if not usuario or not pwd_context.verify(req.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    
    token = jwt.encode({"sub": usuario.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/dashboard/stats", response_model=DashboardStatsSchema)
def get_stats(db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    total_processos = db.query(Processo).count()
    prazos_pendentes = db.query(Prazo).filter(Prazo.status == "PENDENTE").count()
    
    limite_urgente = date.today() + timedelta(days=3)
    prazos_urgentes = db.query(Prazo).filter(
        Prazo.status == "PENDENTE",
        Prazo.data_fatal <= limite_urgente
    ).count()

    return {
        "total_processos": total_processos,
        "prazos_pendentes": prazos_pendentes,
        "prazos_urgentes": prazos_urgentes
    }

@app.get("/api/prazos", response_model=list[PrazoSchema])
def listar_prazos(db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    return db.query(Prazo).order_by(Prazo.data_fatal.asc()).all()

@app.post("/api/sincronizar", status_code=status.HTTP_200_OK)
def sincronizar(req: SincronizarOABRequest, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    client = DataJudClient()
    ai_service = LegalAIService()
    raw_processos = client.buscar_por_oab(req.oab_numero, req.oab_uf, req.tribunal)

    novos_processos = 0
    for item in raw_processos:
        cnj = item.get("numeroProcesso")
        if not cnj:
            continue

        processo_existente = db.query(Processo).filter(Processo.numero_cnj == cnj).first()
        if not processo_existente:
            # Extrai texto das movimentações para a IA analisar
            movs = item.get("movimentos", [])
            movs_texto = "\n".join([m.get("complemento", m.get("nome", "")) for m in movs[-5:]])
            
            # Executa a IA (Fase 2 e 3) para obter resumo e prazos automáticos
            analise_ia = ai_service.analisar_processo(movs_texto or "Processo ajuizado recentemente sem movimentações complexas.")

            novo_proc = Processo(
                numero_cnj=cnj,
                tribunal=req.tribunal.upper(),
                classe=item.get("classe", {}).get("nome", "Não informada"),
                orgao_julgador=item.get("orgaoJulgador", {}).get("nome", "Não informado"),
                resumo_ia=analise_ia.get("resumo")
            )
            db.add(novo_proc)
            db.flush() # Gera o ID do processo para associar ao prazo

            # Se a IA detectou um prazo válido, cadastra automaticamente na tabela de prazos
            if analise_ia.get("tem_prazo"):
                dias = analise_ia.get("dias_uteis", 5)
                hoje = date.today()
                data_fatal = hoje + timedelta(days=dias)
                
                novo_prazo = Prazo(
                    processo_id=novo_proc.id,
                    descricao=analise_ia.get("descricao_prazo", "Prazo processual identificado por IA"),
                    data_inicio=hoje,
                    data_fatal=data_fatal,
                    dias_uteis=dias,
                    status="URGENTE" if analise_ia.get("urgencia") == "ALTA" else "PENDENTE"
                )
                db.add(novo_prazo)

            novos_processos += 1

    db.commit()
    return {"message": "Sincronização com IA concluída com sucesso.", "novos_adicionados": novos_processos}