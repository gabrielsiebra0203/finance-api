
from fastapi import FastAPI

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

