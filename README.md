
# Finance API

API REST para gerenciamento de transações financeiras pessoais, desenvolvida com Python, FastAPI, SQLAlchemy e PostgreSQL.

## Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Psycopg
- Pydantic
- Pytest
- Uvicorn

## Funcionalidades

- Cadastrar transações financeiras
- Listar transações
- Buscar transações por ID
- Atualizar transações
- Excluir transações
- Validar os dados recebidos
- Persistir informações no PostgreSQL
- Executar testes automatizados com banco isolado

## Estrutura do projeto

```text
finance-api/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── db_models.py
│   ├── db_connection.py
│   ├── criar_tabelas.py
│   ├── consultar_transacoes.py
│   ├── testar_insercao.py
│   └── routers/
│       └── transacoes.py
├── tests/
│   ├── conftest.py
│   ├── db_test.py
│   ├── preparar_banco.py
│   ├── test_main.py
│   ├── test_validacoes.py
│   ├── test_isolamento_db.py
│   └── test_transacoes_db.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd finance-api
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar o PostgreSQL

Crie os bancos:

- `finance_db`
- `finance_test_db`

Crie um usuário PostgreSQL com permissões sobre esses bancos.

### 5. Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis de acordo com sua instalação do PostgreSQL.

A senha real deve ficar somente no arquivo `.env`, que não é versionado.

### 6. Criar as tabelas

Banco de desenvolvimento:

```bash
python -m app.criar_tabelas
```

Banco de testes:

```bash
python -m tests.preparar_banco
```

### 7. Executar a API

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Acesse a documentação interativa:

http://localhost:8001/docs

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | / | Informações iniciais |
| GET | /health | Verificação de saúde |
| GET | /sobre | Informações do projeto |
| GET | /transacoes | Listar transações |
| POST | /transacoes | Cadastrar transação |
| GET | /transacoes/{id} | Buscar por ID |
| PUT | /transacoes/{id} | Atualizar transação |
| DELETE | /transacoes/{id} | Excluir transação |

## Exemplo de cadastro

POST /transacoes

```json
{
  "descricao": "Compra de notebook",
  "valor": "2500.00",
  "tipo": "despesa"
}
```

Os tipos permitidos são `receita` e `despesa`.

## Testes automatizados

Execute:

```bash
python -m pytest -q
```

O projeto possui 26 testes automatizados cobrindo endpoints, validações e operações com PostgreSQL.

Os testes utilizam o banco `finance_test_db`, com isolamento por transações e rollback.

## Autor

Gabriel Braga Siebra

Projeto desenvolvido como parte dos estudos de desenvolvimento backend com Python.
