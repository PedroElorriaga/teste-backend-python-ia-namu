# Assistente de Recomendação de Bem-Estar com IA — Namu

API REST desenvolvida com **FastAPI** e **PostgreSQL** que oferece recomendações personalizadas de atividades de bem-estar com base no perfil do usuário, com suporte a histórico de recomendações e coleta de feedbacks.

---

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura e Estrutura](#arquitetura-e-estrutura)
- [Modelos de Dados](#modelos-de-dados)
- [Endpoints da API](#endpoints-da-api)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Migrações com Alembic](#migrações-com-alembic)
- [Testes](#testes)
- [Decisões Técnicas](#decisões-técnicas)
- [Estado Atual e Próximos Passos](#estado-atual-e-próximos-passos)

---

## Sobre o Projeto

Este projeto é uma API de recomendações de bem-estar que recebe o perfil de um usuário (objetivos, restrições, nível de experiência) e, com base nesses dados, gera sugestões de atividades personalizadas utilizando um LLM (modelo de linguagem) via Ollama.

O projeto foi construído como teste técnico para a vaga de Desenvolvedor Backend Python com foco em IA na Namu.

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Justificativa |
|---|---|---|
| **Python** | 3.11 | Versão LTS estável com suporte completo a tipagem e asyncio |
| **FastAPI** | 0.135.1 | Alta performance, validação automática com Pydantic, documentação Swagger nativa |
| **SQLAlchemy** | 2.0.43 | ORM maduro com suporte a tipos PostgreSQL nativos (ex: `ARRAY`) |
| **PostgreSQL** | 16 | Banco relacional robusto com suporte a arrays e tipos customizados |
| **psycopg2-binary** | 2.9.10 | Driver PostgreSQL mais utilizado para Python |
| **Alembic** | latest | Controle de versão e migrações do schema do banco de dados |
| **Uvicorn** | 0.41.0 | Servidor ASGI de alta performance para FastAPI |
| **Ollama** | latest | Servidor local para execução de modelos LLM (ex: `llama3.2`, `mistral`) |
| **pytest** | 9.0.2 | Framework de testes com suporte a fixtures, monkeypatch e parametrização |
| **Pipenv** | — | Gerenciamento de dependências e ambientes virtuais |

---

## Arquitetura e Estrutura

O projeto segue uma arquitetura **modular por domínio**, com separação clara de responsabilidades em camadas:

```
src/
├── database/           # Configuração da conexão com o banco (SessionLocal, Base, get_db)
├── main/               # Ponto de entrada da aplicação FastAPI
└── modules/
    ├── users/          # Módulo de usuários
    │   ├── controller/ # Orquestra requisições, valida DTOs
    │   ├── dtos/       # Schemas Pydantic de entrada e saída
    │   ├── models/     # Modelos ORM (SQLAlchemy)
    │   ├── repositories/ # Acesso direto ao banco de dados
    │   └── router/     # Definição das rotas HTTP
    └── recommendations/ # Módulo de recomendações
        ├── controller/
        ├── dtos/
        ├── models/
        ├── repositories/
        ├── router/
        └── services/    # Integração com serviços externos (ex: Ollama LLM)
```

**Padrão adotado**: `Router → Controller → Service / Repository`

- **Router**: recebe a requisição HTTP, delega ao controller e formata a resposta
- **Controller**: recebe DTOs tipados, normaliza campos opcionais vazios e orquestra a lógica de negócio
- **Service**: integração com serviços externos (ex: Ollama LLM)
- **Repository**: único ponto de acesso ao banco de dados

---

## Modelos de Dados

### `users`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `name` | String(50) | Nome do usuário (único) |
| `age` | Integer | Idade |
| `goals` | ARRAY(String) | Objetivos de bem-estar (ex: "reduzir estresse") |
| `restrictions` | String(255) | Restrições de saúde ou físicas (opcional) |
| `experience_level` | Enum | `iniciante`, `intermediário` ou `avançado` |
| `created_at` | DateTime | Data de criação (automática) |

### `recommendations`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `user_id` | Integer (FK) | Referência ao usuário |
| `name` | String(50) | Nome da atividade recomendada |
| `description` | String(255) | Descrição da atividade |
| `duration` | Float | Duração em minutos |
| `category` | String(64) | Categoria (ex: "Cardio", "Yoga") |
| `reasoning` | String(255) | Justificativa da recomendação pela IA |
| `precautions` | String(255) | Alertas com base nas restrições do usuário |
| `created_at` | DateTime | Data de criação (automática) |

### `recommendation_feedbacks`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `recommendation_id` | Integer (FK) | Referência à recomendação avaliada |
| `rating` | Integer | Avaliação de 1 a 5 |
| `comment` | String(255) | Comentário do usuário |
| `created_at` | DateTime | Data de criação (automática) |

---

## Endpoints da API

A documentação interativa completa está disponível via Swagger em `http://localhost:8000/docs` após subir a aplicação.

### Usuários

#### `POST /users/`
Cria um novo usuário com perfil de bem-estar.

**Request body:**
```json
{
  "name": "Ana Costa",
  "age": 28,
  "goals": ["reduzir estresse", "melhorar sono"],
  "restrictions": "Nenhuma",
  "experience_level": "iniciante"
}
```

Observação: `restrictions` é opcional. Se enviado como string vazia ou apenas espaços, o valor é normalizado para `null`.

**Response (201):**
```json
{
  "message": "Usuario criado",
  "user": {
    "id": 1,
    "name": "Ana Costa",
    "age": 28,
    "goals": ["reduzir estresse", "melhorar sono"],
    "restrictions": "Nenhuma",
    "experience_level": "iniciante"
  }
}
```

---

#### `GET /users/{user_id}/recommendations`
Retorna o histórico de recomendações de um usuário.

**Response (200):**
```json
{
  "message": "Histórico de recomendações do usuário 1",
  "recommendations": [
    {
      "id": 1,
      "name": "Caminhada",
      "description": "Caminhada leve de 30 minutos",
      "duration": 30.0,
      "category": "Cardio",
      "reasoning": "Indicado para redução de estresse.",
      "precautions": "Hidrate-se antes de começar."
    }
  ]
}
```

---

### Recomendações

#### `POST /recommendations/`
Gera uma nova recomendação personalizada para o usuário. Retorna 404 se o `user_id` não existir.

**Request body:**
```json
{
  "user_id": 1,
  "additional_info": "Estou com dor nas costas hoje"
}
```

Observação: `additional_info` é opcional. Se enviado como string vazia ou apenas espaços, o valor é normalizado para `null`.

**Response (201):**
```json
{
  "message": "Recomendação criada",
  "response": {
    "activities": [
      {
        "name": "Caminhada",
        "description": "Caminhada leve de 30 minutos",
        "duration": 30.0,
        "category": "Cardio"
      }
    ],
    "reasoning": "Atividade indicada para o perfil do usuário.",
    "precautions": "Evite impacto por causa das restrições informadas."
  }
}
```

---

#### `POST /recommendations/{recommendation_id}/feedback`
Registra um feedback do usuário sobre uma recomendação. Retorna 404 se a recomendação não existir.

**Request body:**
```json
{
  "rating": 4,
  "comment": "Gostei muito da recomendação!"
}
```

**Response (201):**
```json
{
  "message": "Feedback criado",
  "response": {
    "id": 1,
    "recommendation_id": 1,
    "rating": 4,
    "comment": "Gostei muito da recomendação!"
  }
}
```

---

## Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose
- [Python 3.11+](https://www.python.org/)
- [Pipenv](https://pipenv.pypa.io/) (instalação: `pip install pipenv`)

---

## Instalação e Execução

### 1. Clone o repositório

```bash
git clone <url-do-repositório>
cd teste-backend-python-ia-namu
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```bash
cp .env.example .env
```

Preencha as variáveis conforme descrito na seção [Variáveis de Ambiente](#variáveis-de-ambiente).

### 3. Suba os serviços (banco + Ollama)

```bash
docker-compose up -d
```

Isso sobe:
- **PostgreSQL** na porta configurada em `DB_PORT`, com o script `seed.sql` executado automaticamente na primeira inicialização (5 perfis de exemplo)
- **Ollama** na porta `11434`, servindo modelos LLM localmente
- **ollama_init** que faz o download automático do modelo definido em `LLM_MODEL` (padrão: `llama3.2`)

### 4. Instale as dependências

```bash
pipenv install
```

### 5. Execute as migrações

```bash
pipenv run alembic upgrade head
```

### 6. Inicie a aplicação

```bash
pipenv run start
```

A API estará disponível em `http://localhost:8000`.  
Documentação Swagger em `http://localhost:8000/docs`.

---

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `DB_USER` | Usuário do PostgreSQL | `namu` |
| `DB_PASSWORD` | Senha do PostgreSQL | `namu123` |
| `DB_HOST` | Host do PostgreSQL | `localhost` |
| `DB_PORT` | Porta do PostgreSQL | `5434` |
| `DB_NAME` | Nome do banco de dados | `namu_ai` |
| `LLM_MODEL` | Modelo LLM utilizado pelo Ollama e pelo service (configurável) | `llama3.2`, `mistral`, `gemma2` |
| `LLM_API_KEY` | Chave de API para provedores na nuvem (reservado para uso futuro) | — |
| `OLLAMA_BASE_URL` | URL base do servidor Ollama | `http://localhost:11434` |

---

## Migrações com Alembic

O controle do schema do banco é feito via Alembic. As migrações estão em `alembic/versions/` e cobrem:

1. Criação da tabela `recommendations`
2. Adição da FK `user_id` em `recommendations`
3. Remoção da constraint `UNIQUE` no nome da recomendação
4. Criação da tabela `recommendation_feedbacks`

Para aplicar todas as migrações:
```bash
pipenv run alembic upgrade head
```

Para reverter a última migração:
```bash
pipenv run alembic downgrade -1
```

---

## Testes

Os testes utilizam **pytest** com banco de dados completamente mockado (sem dependência de PostgreSQL em execução). O `conftest.py` injeta um `TestClient` do FastAPI com a sessão de banco substituída por um `Mock`.

Atualmente a suíte também cobre o contrato introduzido pelos DTOs Pydantic nas rotas/controllers, a normalização de campos opcionais vazios e a presença do `id` no histórico de recomendações.

Para executar:
```bash
pipenv run test
```

A suíte de testes cobre:
- Roteamento (routers) de usuários e recomendações
- Controllers de usuários e recomendações
- Repositories de usuários e recomendações
- Service de integração com Ollama (OllamaRecommendationService)
- Casos de sucesso, erros 404 e erros de validação 422

---

## Decisões Técnicas

**FastAPI sobre Flask/Django**: FastAPI foi escolhido pela validação automática via Pydantic, geração automática de documentação OpenAPI/Swagger, suporte nativo a async/await e tipagem estática, o que acelera o desenvolvimento e reduz bugs.

**SQLAlchemy com sessão síncrona**: Optei por `SessionLocal` síncrono em vez de async para simplificar a integração inicial com PostgreSQL, sem perda funcional para o escopo do projeto.

**SQL raw via `sqlalchemy.text()` em queries específicas**: Algumas operações do repositório utilizam SQL raw com parâmetros nomeados (`:param`) em vez do ORM. Isso foi adotado em consultas simples de leitura (`get_user_by_id`) e inserts com `RETURNING` (`create_recommendation_feedback`) para manter controle explícito sobre o SQL gerado e evitar overhead do ORM onde não é necessário.

**Pydantic para DTOs**: Todos os dados de entrada e saída usam schemas Pydantic separados dos modelos ORM, garantindo separação entre a camada de persistência e a camada HTTP.

**Alembic para migrações**: O schema evolui via migrations versionadas, permitindo rastrear e reverter mudanças de banco com segurança.

**Testes com mock de DB**: Os testes de router, controller e repository usam `monkeypatch` e `Mock` para isolar cada camada, tornando a suíte rápida e sem dependências externas.

---

## Estado Atual e Próximos Passos

### Implementado ✅
- Cadastro de usuários com validação de perfil
- Geração de recomendações personalizadas via LLM (Ollama)
- Histórico de recomendações por usuário
- Endpoint de feedback com persistência via SQL raw (`INSERT ... RETURNING`)
- Consultas com SQL raw parametrizado (`sqlalchemy.text()`) no repositório
- Migrações de banco via Alembic
- Testes automatizados com cobertura de routers, controllers, repositories e service
- Documentação automática via Swagger (`/docs`)

### Onde Utilizei IA para me auxiliar 🤖
- Testes (Por conta do curto período, preferi focar na construção da API e conexão com o LLM -> OBS mesmo assim acompanhei quais mudanças e testes foram cobertos e porque)
- Criação desta documentação (Para facilidade e eficiência)
- Arquivos de migração do alembic (Por receio de perder informações ou erros na hora de migrar, decidi usar a IA como um braço direito na concepção desses arquivos)
- Docker compose (Utilizei para otimizar meu tempo na hora da criação dos serviços e download do LLM model)
- CI (Ocorreram alguns erros inesperados no Actions do GitHub, então utilizei a IA para debugar o problema)
- System Content (Na hora de definir passei parametros que eu achava importante e pedi para a IA refinar alguns pontos para mim)
