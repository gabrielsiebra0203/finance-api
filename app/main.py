from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal

# Inicialização da aplicação
app = FastAPI(
    title="Finance API",
    description="API REST para gerenciamento financeiro pessoal",
    version="1.0.0"
)


# Rota inicial
@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo à Finance API",
        "status": "online"
    }


# Rota para verificar se a API está funcionando
@app.get("/health")
def verificar_saude():
    return {
        "status": "ok",
        "servico": "finance-api"
    }


# Rota com informações sobre o projeto
@app.get("/sobre")
def sobre():
    return {
        "projeto": "Finance API",
        "versao": "1.0.0",
        "objetivo": "Controle financeiro pessoal"
    }

# Lista temporária de transações financeiras
transacoes = [
    {
        "id": 1,
        "descricao": "Salário",
        "valor": 3000.00,
        "tipo": "receita"
    },
    {
        "id": 2,
        "descricao": "Supermercado",
        "valor": 250.00,
        "tipo": "despesa"
    }
]


# Listar todas as transações
@app.get("/transacoes")
def listar_transacoes():
    return {
        "total": len(transacoes),
        "transacoes": transacoes
    }


# Modelo para receber os dados de uma nova transação
class TransacaoEntrada(BaseModel):
    descricao: str = Field(min_length=1, max_length=100)
    valor: Decimal = Field(
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2
    )
    tipo: Literal["receita", "despesa"]



# Cadastrar uma nova transação
@app.post("/transacoes", status_code=status.HTTP_201_CREATED)
def criar_transacao(transacao: TransacaoEntrada):
    novo_id = max(
        (item["id"] for item in transacoes),
        default=0
    ) + 1

    nova_transacao = {
        "id": novo_id,
        **transacao.model_dump()
    }

    transacoes.append(nova_transacao)

    return nova_transacao


# Consultar uma transação pelo ID
@app.get("/transacoes/{transacao_id}")
def buscar_transacao(transacao_id: int):

    for transacao in transacoes:
        if transacao["id"] == transacao_id:
            return transacao

    raise HTTPException(
        status_code=404,
        detail="Transação não encontrada"
    )


# Atualizar uma transação existente
@app.put("/transacoes/{transacao_id}")
def atualizar_transacao(
    transacao_id: int,
    dados: TransacaoEntrada
):
    for transacao in transacoes:
        if transacao["id"] == transacao_id:
            transacao.update(dados.model_dump())
            return transacao

    raise HTTPException(
        status_code=404,
        detail="Transação não encontrada"
    )

@app.delete("/transacoes/{transacao_id}")
def excluir_transacao(transacao_id: int):

    for transacao in transacoes:
        if transacao["id"] == transacao_id:
            transacoes.remove(transacao)

            return {
                "mensagem": "Transação excluída com sucesso",
                "id": transacao_id
            }

    raise HTTPException(
        status_code=404,
        detail="Transação não encontrada"
    )