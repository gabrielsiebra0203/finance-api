from typing import Literal
from decimal import Decimal
from fastapi import APIRouter, HTTPException, status, Depends, Query


from app.models import (
    TransacaoEntrada,
    TransacaoSaida,
    ListaTransacoesSaida,
    ResumoFinanceiroSaida,
)
from app.services.resumo_financeiro import calcular_resumo_financeiro

from sqlalchemy import select, func
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
    limit: int | None = Query(
        default=None,
        ge=1,
        le=100,
        description="Quantidade máxima de transações retornadas"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Quantidade de transações ignoradas"
    ),
    
    ordenar_por: Literal["id", "valor", "descricao"] = Query(
        default="id",
        description="Campo utilizado para ordenar as transações"
    ),

    ordem: Literal["asc", "desc"] = Query(
        default="asc",
        description="Direção da ordenação: crescente ou decrescente"
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

    # Conta os registros após aplicar os filtros
    comando_contagem = select(func.count()).select_from(
        comando.order_by(None).subquery()
    )

    total = db.scalar(comando_contagem)

    # Ordena os registros para a paginação
    
    campos_ordenacao = {
        "id": Transacao.id,
        "valor": Transacao.valor,
        "descricao": Transacao.descricao
    }

    campo_selecionado = campos_ordenacao[ordenar_por]

    if ordem == "desc":
        campo_ordenado = campo_selecionado.desc()
    else:
        campo_ordenado = campo_selecionado.asc()

    comando = comando.order_by(
        campo_ordenado,
        Transacao.id.asc()
    )


    # Ignora os primeiros registros
    comando = comando.offset(offset)

    # Limita a quantidade retornada, quando solicitado
    if limit is not None:
        comando = comando.limit(limit)

    
    transacoes_db = db.scalars(comando).all()

    tem_proxima = (
        offset + len(transacoes_db) < total
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "tem_proxima": tem_proxima,
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
    "/resumo",
    response_model=ResumoFinanceiroSaida,
    summary="Consultar resumo financeiro",
    description="Retorna o total de receitas, despesas e saldo financeiro."
)
def obter_resumo_financeiro(
    db: Session = Depends(get_db)
):
    return calcular_resumo_financeiro(db)


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
