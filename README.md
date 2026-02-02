# MAI - Marketing Artificial Intelligence

> **Decision Intelligence** para Marketing e Crescimento.  
> IA Estratégica que protege caixa e acelera crescimento sustentável.

---

## 🎯 Visão Geral

MAI é uma plataforma de Decision Intelligence focada em:
- **Decisões Estratégicas**: avalia decisões de marketing com impacto real
- **MAI Decision Score™**: scoring determinístico (Impacto × Urgência ÷ Risco)
- **Validação Cruzada**: segunda opinião estratégica
- **RAG Multi-Namespace**: conhecimento proprietário segmentado
- **Integração Ads**: Google Ads, Meta Ads, TikTok Ads, Retail Media
- **SEO & Ferramentas**: SEMrush integration
- **Ecommerce**: VTEX, Mercado Livre, Nuvemshop, Tray, Loja Integrada

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Next.js)                      │
│    Landing Page │ Auth Pages │ Dashboard │ Integrations      │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                        │
├─────────────────────────────────────────────────────────────┤
│  Motor MAI                                                   │
│  ├── Decision Orchestrator                                  │
│  ├── RAG Engine (multi-namespace)                           │
│  ├── Scoring Engine (Impacto × Urgência ÷ Risco)           │
│  └── Cross Validation Engine                                │
├─────────────────────────────────────────────────────────────┤
│  Agentes Estratégicos                                        │
│  ├── Growth & Capital        ├── Behavioral & Demand        │
│  ├── Performance Revenue     ├── Market Sizing              │
│  ├── Funnel Economics        └── Unit Economics             │
├─────────────────────────────────────────────────────────────┤
│  Integrações                                                 │
│  ├── Ads: Google, Meta, TikTok, Programmatic, Retail Media      │
│  ├── Ecommerce: VTEX, Mercado Livre, Nuvemshop, Tray, LI    │
│  └── Tools: SEMrush                                         │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│  PostgreSQL  │  Redis  │  Qdrant (Vector DB)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: http://localhost:3000

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Edite o arquivo .env com suas configurações

# Iniciar servidor
uvicorn app.main:app --reload
```

Acesse API: http://localhost:8000  
Docs (Swagger): http://localhost:8000/docs

---

## 📚 Estrutura do Projeto

```
PROJETO/
├── frontend/                    # Next.js 14 + TailwindCSS
│   ├── src/
│   │   ├── app/                # App Router
│   │   │   ├── auth/           # Login, Register, Password
│   │   │   ├── dashboard/      # Dashboard Principal & Decisões
│   │   │   ├── integrations/   # Gestão de Integrações
│   │   │   └── page.tsx        # Landing Page
│   │   ├── components/         # React Components (UI, Landing, Charts)
│   │   │   ├── ui/             # Button, Card, Logo
│   │   │   └── landing/        # Hero, Problem, Benefits, etc.
│   │   └── lib/                # Utilities & Hooks
│   └── tailwind.config.ts      # TailwindCSS config (MAI theme)
│
├── backend/                     # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── api/v1/             # API Endpoints
│   │   │   ├── auth.py         # Autenticação
│   │   │   ├── decisions.py    # Avaliação e Scoring
│   │   │   ├── users.py        # Profile, API Keys
│   │   │   ├── campaigns.py    # Sincronização de Ads
│   │   │   ├── knowledge.py    # RAG e Princípios
│   │   │   └── integrations.py # Configuração de Plugins
│   │   ├── core/               # Security, RBAC
│   │   ├── engine/             # MAI Decision Engine
│   │   │   ├── orchestrator.py # Central Pipeline
│   │   │   ├── rag_engine.py   # Knowledge Retrieval
│   │   │   ├── scoring_engine.py    # MAI Score™
│   │   │   └── validation_engine.py # Cross Validation
│   │   ├── agents/             # Strategic Agents
│   │   ├── integrations/       # Conectores (Ads, Ecommerce, Tools)
│   │   ├── models/             # SQLAlchemy Models
│   │   └── schemas/            # Pydantic Schemas
│   └── requirements.txt
│
└── README.md
```

---

## 🔐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Criar conta |
| POST | `/api/v1/auth/login` | Login (retorna JWT) |
| POST | `/api/v1/auth/forgot-password` | Solicitar reset |
| POST | `/api/v1/auth/reset-password` | Redefinir senha |
| POST | `/api/v1/auth/verify-email` | Verificar email |
| POST | `/api/v1/auth/refresh` | Renovar token |

### Decisions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/decisions/evaluate` | Avaliar decisão estratégica |
| POST | `/api/v1/decisions/score` | Calcular MAI Score™ |
| POST | `/api/v1/decisions/validate` | Cross-validation |
| GET | `/api/v1/decisions/history` | Histórico de decisões |

### Campaigns & Integrations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/campaigns` | Listar campanhas |
| POST | `/api/v1/campaigns/sync/google` | Sincronizar Google Ads |
| POST | `/api/v1/campaigns/sync/meta` | Sincronizar Meta Ads |
| POST | `/api/v1/campaigns/sync/tiktok` | Sincronizar TikTok Ads |
| GET | `/api/v1/integrations` | Listar integrações disponíveis |
| POST | `/api/v1/integrations/config` | Configurar credenciais |

### Knowledge (RAG)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/knowledge/namespaces` | Listar domínios de conhecimento |
| GET | `/api/v1/knowledge/principles` | Listar princípios estratégicos |
| GET | `/api/v1/knowledge/namespaces/{id}/search` | Pesquisar no RAG |

---

## 🧪 MAI Decision Score™

O MAI Score calcula a prioridade de uma decisão usando:

```
MAI Score = (Impacto × Urgência) ÷ Risco
```

### Interpretação
| Score | Decisão |
|-------|---------|
| ≥ 6 | **EXECUTAR** - Sinal verde |
| 3-5.9 | **AJUSTAR** - Validar premissas |
| < 3 | **PAUSAR** - Alto risco / baixo impacto |

### Dimensões (1-5)
- **Impacto**: Potencial financeiro e estratégico
- **Risco**: Exposição negativa e reversibilidade
- **Urgência**: Sensibilidade ao tempo

---

## 🎨 Design System

O frontend usa uma paleta dark premium:

| Cor | Hex | Uso |
|-----|-----|-----|
| MAI Primary | `#6366F1` | Accent, botões |
| Dark BG | `#0A0A0F` | Background principal |
| Glass | `rgba(255,255,255,0.05)` | Cards, overlays |

---

## 📄 Licença

Proprietary - MAI © 2024
