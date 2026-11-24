
from fastapi import FastAPI

from app.routers.transacoes import router as transacoes_router


app = FastAPI(
    title="Finance API",
    description="API REST para gerenciamento financeiro pessoal",
    version="1.0.0"
)


# Registra as rotas de transações
app.include_router(transacoes_router)


@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo à Finance API",
        "status": "online"
    }


@app.get("/health")
def verificar_saude():
    return {
        "status": "ok",
        "servico": "finance-api"
    }


@app.get("/sobre")
def sobre():
    return {
        "projeto": "Finance API",
        "versao": "1.0.0",
        "objetivo": "Controle financeiro pessoal"
    }
