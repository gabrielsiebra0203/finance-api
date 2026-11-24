
from fastapi import APIRouter, HTTPException, status

from app.models import TransacaoEntrada
from app.database import transacoes


router = APIRouter(
    prefix="/transacoes",
    tags=["Transações"]
)


@router.get("")
def listar_transacoes():
    return {
        "total": len(transacoes),
        "transacoes": transacoes
    }


@router.post("", status_code=status.HTTP_201_CREATED)
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


@router.get("/{transacao_id}")
def buscar_transacao(transacao_id: int):
    for transacao in transacoes:
        if transacao["id"] == transacao_id:
            return transacao

    raise HTTPException(
        status_code=404,
        detail="Transação não encontrada"
    )


@router.put("/{transacao_id}")
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


@router.delete("/{transacao_id}")
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
