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
- Filtrar transações por tipo (receita ou despesa)
- Filtrar transações por categoria
- Filtrar transações por valor mínimo e máximo
- Combinar múltiplos filtros em uma consulta
- Validar parâmetros de consulta e intervalos monetários
- Paginação de transações com `limit` e `offset`
- Contagem otimizada com `COUNT(*)` no PostgreSQL
- Metadados de paginação (`total`, `limit`, `offset`, `tem_proxima`)
- Paginação combinada com filtros de tipo, categoria e valores
- Validação automática dos parâmetros de paginação
### Ordenação de transações

A API permite ordenar transações pelos seguintes campos:

- `id`: identificador da transação
- `valor`: valor financeiro
- `descricao`: descrição da transação

A direção pode ser:

- `asc`: ordem crescente (padrão)
- `desc`: ordem decrescente

Exemplos:

GET /transacoes?ordenar_por=valor&ordem=desc

GET /transacoes?ordenar_por=descricao&ordem=asc

GET /transacoes?tipo=despesa&ordenar_por=valor&ordem=desc&limit=5&offset=0

A ordenação pode ser combinada com filtros e paginação.

Parâmetros inválidos retornam HTTP 422.

Quando não são informados parâmetros de ordenação,
a API utiliza `id` em ordem crescente.
### Resumo financeiro

A Finance API disponibiliza um endpoint para consultar os principais indicadores financeiros.

**Endpoint:**

`GET /transacoes/resumo`

**Exemplo de resposta:**

```json
{
  "total_receitas": "4300.00",
  "total_despesas": "1750.00",
  "saldo": "2550.00"
}
```

**Indicadores:**

- `total_receitas`: soma de todas as receitas cadastradas.
- `total_despesas`: soma de todas as despesas cadastradas.
- `saldo`: diferença entre receitas e despesas.

**Implementação técnica:**

- FastAPI para disponibilização do endpoint.
- SQLAlchemy para construção das consultas.
- PostgreSQL para armazenamento e agregação dos dados.
- Função SQL `SUM()` para cálculo dos totais.
- `Decimal` para precisão monetária.
- Pydantic para validação e serialização da resposta.
- Camada de serviços separada das rotas HTTP.

**Testes automatizados:**

O resumo financeiro possui testes para os seguintes cenários:

- Banco sem transações.
- Apenas receitas cadastradas.
- Apenas despesas cadastradas.
- Receitas e despesas combinadas.

**Total do projeto: 65 testes automatizados.**

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

## Filtros de transações

O endpoint `GET /transacoes` permite consultar transações utilizando filtros opcionais.

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `tipo` | string | `receita` ou `despesa` |
| `categoria` | string | Categoria da transação |
| `valor_min` | decimal | Valor mínimo, inclusive |
| `valor_max` | decimal | Valor máximo, inclusive |

## Paginação de transações

O endpoint `GET /transacoes` permite consultar transações financeiras utilizando paginação e filtros dinâmicos.

### Parâmetros

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `limit` | int (opcional) | Quantidade máxima de registros retornados, entre 1 e 100 |
| `offset` | int | Quantidade de registros ignorados. Padrão: 0 |

Quando `limit` não é informado, todas as transações correspondentes aos filtros são retornadas.

### Exemplos de requisições

**Primeira página:**

```http
GET /transacoes?limit=5&offset=0
```

**Segunda página:**

```http
GET /transacoes?limit=5&offset=5
```

**Paginação com filtros combinados:**

```http
GET /transacoes?tipo=despesa&valor_min=50&valor_max=500&limit=5&offset=0
```

### Exemplo de resposta

```json
{
  "total": 12,
  "limit": 2,
  "offset": 0,
  "tem_proxima": true,
  "transacoes": [
    {
      "id": 1,
      "descricao": "Supermercado",
      "valor": "250.00",
      "tipo": "despesa",
      "categoria": "Alimentação"
    },
    {
      "id": 2,
      "descricao": "Transporte",
      "valor": "50.00",
      "tipo": "despesa",
      "categoria": "Transporte"
    }
  ]
}
```

O campo `total` representa a quantidade de registros que correspondem aos filtros antes da paginação.

O campo `tem_proxima` indica se existem mais registros após a página atual.

A contagem utiliza `COUNT(*)` no PostgreSQL, evitando carregar todos os registros na memória da aplicação.

### Validações

A API retorna HTTP 422 quando:

- `limit` é menor que 1 ou maior que 100.
- `offset` é negativo.
- Os parâmetros recebem valores incompatíveis com seus tipos.

Quando o `offset` ultrapassa a quantidade de registros encontrados, a API retorna HTTP 200 com uma lista vazia.

### Exemplos

**Filtrar despesas:**

```http
GET /transacoes?tipo=despesa
```

**Filtrar por categoria:**

```http
GET /transacoes?categoria=Alimentação
```

**Filtrar por intervalo de valores:**

```http
GET /transacoes?valor_min=100&valor_max=500
```

**Combinar todos os filtros:**

```http
GET /transacoes?tipo=despesa&categoria=Alimentação&valor_min=100&valor_max=500
```

Os filtros são opcionais e podem ser combinados.

O endpoint retorna HTTP `422` quando recebe parâmetros inválidos, incluindo valores negativos, tipos não permitidos e intervalos em que `valor_min` é maior que `valor_max`.

Consultas válidas sem correspondências retornam HTTP `200`, com `total: 0` e uma lista vazia.

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

O projeto possui **61 testes automatizados**, cobrindo:

- Endpoints REST
- Operações CRUD
- Validações Pydantic
- Persistência com PostgreSQL
- Isolamento do banco de testes
- Categorias financeiras
- Contratos de resposta
- Documentação OpenAPI
- Filtros finaceiros e funcionalidades testadas

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