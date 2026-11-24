# Finance API

API REST para gerenciamento de transações financeiras pessoais, desenvolvida com Python, FastAPI, SQLAlchemy e PostgreSQL.

O projeto foi criado como parte dos meus estudos de desenvolvimento backend com Python, aplicando conceitos de APIs REST, persistência de dados, validação, migrações de banco de dados, documentação e testes automatizados.

## Tecnologias utilizadas

- **Python** — Linguagem principal
- **FastAPI** — Desenvolvimento da API REST
- **PostgreSQL** — Banco de dados relacional
- **SQLAlchemy ORM** — Mapeamento e persistência dos dados
- **Alembic** — Controle de versões e migrações do banco
- **Psycopg** — Conexão com PostgreSQL
- **Pydantic** — Validação e serialização de dados
- **Pytest** — Testes automatizados
- **Uvicorn** — Servidor ASGI
- **Swagger/OpenAPI** — Documentação automática da API

## Funcionalidades

- Cadastrar receitas e despesas
- Listar transações financeiras
- Buscar transações por ID
- Atualizar transações existentes
- Excluir transações
- Classificar transações por categorias opcionais
- Validar valores monetários com `Decimal`
- Validar descrições, tipos e categorias
- Persistir informações no PostgreSQL
- Gerenciar alterações no banco com Alembic
- Padronizar respostas com schemas Pydantic
- Documentar endpoints automaticamente com OpenAPI
- Executar testes automatizados com banco isolado e rollback

## Estrutura do projeto

```text
finance-api/
├── alembic/
│   ├── versions/
│   │   ├── 608f683a3cb2_estrutura_inicial_de_transacoes.py
│   │   └── 0fdfd41f4d0f_adiciona_categoria_em_transacoes.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/
│   ├── routers/
│   │   └── transacoes.py
│   ├── main.py
│   ├── models.py
│   ├── db_models.py
│   ├── db_connection.py
│   ├── criar_tabelas.py
│   ├── consultar_transacoes.py
│   └── testar_insercao.py
├── tests/
│   ├── conftest.py
│   ├── db_test.py
│   ├── preparar_banco.py
│   ├── test_main.py
│   ├── test_validacoes.py
│   ├── test_isolamento_db.py
│   ├── test_transacoes_db.py
│   ├── test_categorias.py
│   └── test_contratos.py
├── alembic.ini
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/gabrielsiebra0203/finance-api.git
cd finance-api
```

### 2. Criar o ambiente virtual

No Linux ou WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar o PostgreSQL

É necessário possuir o PostgreSQL instalado e em execução.

Crie dois bancos de dados:

- `finance_db` — Desenvolvimento
- `finance_test_db` — Testes automatizados

Configure um usuário PostgreSQL com as permissões necessárias sobre os bancos.

### 5. Configurar variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Exemplo de configuração:

```dotenv
DB_HOST=localhost
DB_PORT=5433
DB_NAME=finance_db
DB_TEST_NAME=finance_test_db
DB_USER=finance_user
DB_PASSWORD=coloque_sua_senha_aqui
```

Adapte os valores conforme sua instalação.

**Importante:** o arquivo `.env` contém credenciais e não deve ser enviado ao GitHub.

## Migrações com Alembic

O Alembic é utilizado para criar e atualizar a estrutura das tabelas de maneira versionada.

### Aplicar migrações no banco de desenvolvimento

```bash
python -m alembic upgrade head
```

### Verificar a revisão atual

```bash
python -m alembic current
```

### Consultar o histórico

```bash
python -m alembic history
```

### Aplicar migrações no banco de testes

```bash
ALEMBIC_USE_TEST_DB=1 python -m alembic upgrade head
```

A variável `ALEMBIC_USE_TEST_DB=1` seleciona explicitamente o banco de testes configurado no projeto.

**Atenção:** o comando `stamp` não é necessário em uma instalação nova. Ele foi utilizado durante a migração inicial dos bancos que já possuíam tabelas.

## Executar a API

Com o ambiente virtual ativado e as migrações aplicadas:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

A API estará disponível em:

http://localhost:8001

Documentação Swagger:

http://localhost:8001/docs

Documentação alternativa ReDoc:

http://localhost:8001/redoc

Especificação OpenAPI:

http://localhost:8001/openapi.json

## Endpoints disponíveis

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Informações iniciais |
| GET | `/health` | Verificação de saúde |
| GET | `/sobre` | Informações do projeto |
| GET | `/transacoes` | Listar transações |
| POST | `/transacoes` | Cadastrar transação |
| GET | `/transacoes/{transacao_id}` | Buscar por ID |
| PUT | `/transacoes/{transacao_id}` | Atualizar transação |
| DELETE | `/transacoes/{transacao_id}` | Excluir transação |

## Exemplo de cadastro

**POST `/transacoes`**

Corpo da requisição:

```json
{
  "descricao": "Compra de notebook",
  "valor": "2500.00",
  "tipo": "despesa",
  "categoria": "Tecnologia"
}
```

Exemplo de resposta HTTP `201 Created`:

```json
{
  "id": 1,
  "descricao": "Compra de notebook",
  "valor": "2500.00",
  "tipo": "despesa",
  "categoria": "Tecnologia"
}
```

O identificador é gerado automaticamente pelo banco.

### Regras de validação

- `descricao`: texto obrigatório entre 1 e 100 caracteres.
- `valor`: número decimal positivo, com até duas casas decimais e 12 dígitos no total.
- `tipo`: aceita somente `receita` ou `despesa`.
- `categoria`: texto opcional entre 1 e 50 caracteres, quando informado.

O valor monetário é representado como string decimal nas respostas dos endpoints de transações.

## Schemas Pydantic

A aplicação utiliza modelos específicos para entrada e saída de dados.

| Schema | Responsabilidade |
|---|---|
| `TransacaoEntrada` | Validar dados recebidos |
| `TransacaoSaida` | Padronizar uma transação retornada |
| `ListaTransacoesSaida` | Padronizar listagens com total e transações |

Os schemas de saída utilizam a serialização do Pydantic, integrada ao FastAPI por meio de `response_model`.

## Testes automatizados

O projeto possui **38 testes automatizados**, cobrindo:

- Endpoints REST
- Operações CRUD
- Validações Pydantic
- Persistência com PostgreSQL
- Isolamento do banco de testes
- Categorias financeiras
- Contratos de resposta
- Documentação OpenAPI

Para executar todos os testes:

```bash
python -m pytest -q
```

Para executar os testes detalhadamente:

```bash
python -m pytest -v
```

Para executar somente os testes de contratos:

```bash
python -m pytest tests/test_contratos.py -v
```

Os testes utilizam o banco `finance_test_db`, separado do banco de desenvolvimento.

O isolamento é realizado com transações e rollback, evitando que os registros criados durante os testes permaneçam no banco.

Antes da execução, configure o banco de testes e aplique suas migrações.

## Versionamento

O projeto utiliza Git e GitHub para acompanhar a evolução do desenvolvimento.

Repositório:

https://github.com/gabrielsiebra0203/finance-api

## Autor

**Gabriel Braga Siebra**

Projeto desenvolvido como parte dos estudos práticos de desenvolvimento backend com Python, FastAPI e PostgreSQL.