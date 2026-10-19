# ⚖️ LegalOps — Dashboard & Monitoramento DataJud / PDPJ

O **LegalOps** é uma aplicação web desenvolvida para advogados e escritórios de advocacia automatizarem a consulta de processos via **DataJud (CNJ)** e gerenciarem seus prazos processuais com cálculo automatizado de dias úteis (CPC).

O projeto foi projetado seguindo uma arquitetura pragmática, limpa e modular (Clean Code / SOLID), focando em alta performance e entrega rápida sem *over-engineering*.

---

## 🚀 Tecnologias Utilizadas

### **Backend**
* **Python 3.10+** / **FastAPI**: Framework web assíncrono e de alta performance.
* **SQLAlchemy 2.0**: ORM para manipulação e persistência de dados.
* **SQLite / PostgreSQL**: Banco de dados relacional (configurável).
* **PyJWT & Passlib (Bcrypt)**: Autenticação segura via tokens JWT e criptografia de senhas.
* **Requests**: Cliente HTTP para comunicação com a API REST do DataJud/CNJ.

### **Frontend**
* **React 18** + **TypeScript**: Interface reativa, modular e fortemente tipada.
* **Vite**: Bundler ultra-rápido para desenvolvimento frontend.
* **Tailwind CSS**: Estilização moderna e responsiva baseada em utilitários.
* **Axios**: Cliente HTTP para consumo da API Backend com interceptors para tokens JWT.

---

## 📌 Funcionalidades Principais

* **🔒 Autenticação & Segurança**: Tela de login com autenticação por Token JWT e armazenamento seguro no `localStorage`.
* **🔄 Sincronização via DataJud**: Integração com a API pública do Conselho Nacional de Justiça (CNJ) para buscar processos por número de OAB, UF e Tribunal (ex: TJSP, TJRJ, TRF3).
* **📊 Dashboard de Métricas**: Indicadores visuais de total de processos, prazos pendentes e alertas de urgência (prazos vencendo em até 3 dias).
* **📅 Calculadora de Prazos Processuais**: Algoritmo para cálculo de data fatal considerando contagem em dias úteis (Art. 219 do CPC).
* **⚡ Interface Responsiva & Moderna**: Tabela dinâmica com destaques visuais (`Badges`) de prioridade e suporte a múltiplos tribunais.

---

## 📂 Estrutura do Projeto

```text
legalops/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py       # Conexão e Sessão SQLAlchemy
│   │   ├── models.py         # Modelos do Banco (Usuario, Processo, Prazo)
│   │   ├── schemas.py        # Validações Pydantic / DTOs
│   │   ├── datajud.py        # Integrador HTTP da API do DataJud
│   │   ├── calculator.py     # Motor de Cálculo de Prazos Processuais (CPC)
│   │   └── main.py          # Endpoints FastAPI e Regras de Autenticação
│   ├── .env                  # Variáveis de ambiente (Chaves de API)
│   └── requirements.txt      # Dependências Python
└── frontend/
    ├── src/
    │   ├── api.ts            # Configuração Axios + Interceptors JWT
    │   ├── App.tsx           # Componente Principal (Login + Dashboard)
    │   ├── main.tsx          # Ponto de entrada React
    │   └── index.css         # Importações do Tailwind CSS
    ├── package.json
    ├── vite.config.ts
    └── tailwind.config.js