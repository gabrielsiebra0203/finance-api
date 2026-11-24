from typing import Literal
from decimal import Decimal
from fastapi import APIRouter, HTTPException, status, Depends, Query


from app.models import (
    TransacaoEntrada,
    TransacaoSaida,
    ListaTransacoesSaida,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_connection import get_db
from app.db_models import Transacao

router = APIRouter(
    prefix="/transacoes",
    tags=["Transações"]
)



@router.get(
    "",
    response_model=ListaTransacoesSaida,
    summary="Listar transações",
    description="Retorna todas as transações financeiras cadastradas."
)



def listar_transacoes(
    tipo: Literal["receita", "despesa"] | None = Query(
        default=None,
        description="Filtrar transações por receita ou despesa"
    ),
    categoria: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Filtrar transações por categoria"
    ),
    valor_min: Decimal | None = Query(
        default=None,
        ge=Decimal("0"),
        description="Valor mínimo da transação"
    ),
    valor_max: Decimal | None = Query(
        default=None,
        ge=Decimal("0"),
        description="Valor máximo da transação"
    ),
    db: Session = Depends(get_db)
):
    if (
        valor_min is not None
        and valor_max is not None
        and valor_min > valor_max
):
        raise HTTPException(
            status_code=422,
            detail="O valor mínimo não pode ser maior que o valor máximo"
    )

    comando = select(Transacao)

    if tipo is not None:
        comando = comando.where(Transacao.tipo == tipo)

    if categoria is not None:
        comando = comando.where(Transacao.categoria == categoria)

    if valor_min is not None:
        comando = comando.where(Transacao.valor >= valor_min)

    if valor_max is not None:
        comando = comando.where(Transacao.valor <= valor_max)

    comando = comando.order_by(Transacao.id)

    transacoes_db = db.scalars(comando).all()

    return {
        "total": len(transacoes_db),
        "transacoes": transacoes_db
    }







@router.post(
    "",
    response_model=TransacaoSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Criar transação",
    description="Cadastra uma receita ou despesa no banco de dados."
)

def criar_transacao(
    transacao: TransacaoEntrada,
    db: Session = Depends(get_db)
):
    nova_transacao = Transacao(
        **transacao.model_dump()
    )

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)

    return nova_transacao




@router.get(
    "/{transacao_id}",
    response_model=TransacaoSaida,
    summary="Buscar transação",
    description="Consulta uma transação financeira pelo seu identificador."
)
def buscar_transacao(
    transacao_id: int,
    db: Session = Depends(get_db)
):
    transacao = db.get(Transacao, transacao_id)

    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    return transacao




@router.put(
    "/{transacao_id}",
    response_model=TransacaoSaida,
    summary="Atualizar transação",
    description="Atualiza os dados de uma transação financeira existente."
)
def atualizar_transacao(
    transacao_id: int,
    dados: TransacaoEntrada,
    db: Session = Depends(get_db)
):
    transacao = db.get(Transacao, transacao_id)

    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    transacao.descricao = dados.descricao
    transacao.valor = dados.valor
    transacao.tipo = dados.tipo
    transacao.categoria = dados.categoria

    db.commit()
    db.refresh(transacao)

    return transacao




@router.delete(
    "/{transacao_id}",
    summary="Excluir transação",
    description="Remove uma transação financeira pelo seu identificador."
)
def excluir_transacao(
    transacao_id: int,
    db: Session = Depends(get_db)
):
    transacao = db.get(Transacao, transacao_id)

    if transacao is None:
        raise HTTPException(
            status_code=404,
            detail="Transação não encontrada"
        )

    db.delete(transacao)
    db.commit()

    return {
        "mensagem": "Transação excluída com sucesso",
        "id": transacao_id
    }
