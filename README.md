# Finance API

API REST de Gestão Financeira desenvolvida com Python e FastAPI.

## Objetivo

Construir uma aplicação para gerenciamento de receitas,
despesas, categorias e relatórios financeiros.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Pytest
- HTTPX

## Funcionalidades implementadas

- GET / - Página inicial
- GET /health - Verificação da API
- GET /sobre - Informações do projeto
- Documentação automática Swagger
- Testes automatizados

## Como executar

1. Criar ambiente virtual:

   python3 -m venv .venv

2. Ativar ambiente:

   source .venv/bin/activate

3. Instalar dependências:

   python -m pip install -r requirements.txt

4. Iniciar servidor:

   python -m uvicorn app.main:app --reload --port 8001

5. Acessar documentação:

   http://127.0.0.1:8001/docs

## Testes

python -m pytest -v

## Próximas funcionalidades

- Cadastro de transações
- Categorias financeiras
- PostgreSQL
- Autenticação JWT
- Relatórios
- Docker
