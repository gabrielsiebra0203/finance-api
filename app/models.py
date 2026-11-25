
from decimal import Decimal
from typing import Literal
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class TransacaoEntrada(BaseModel):
    descricao: str = Field(
        min_length=1,
        max_length=100
    )

    valor: Decimal = Field(
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2
    )

    tipo: Literal["receita", "despesa"]

    categoria: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    data_transacao: date | None = None


class TransacaoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    valor: Decimal
    tipo: Literal["receita", "despesa"]
    categoria: str | None = None
    data_transacao: date



class ListaTransacoesSaida(BaseModel):
    total: int
    limit: int | None = None
    offset: int = 0
    tem_proxima: bool = False
    transacoes: list[TransacaoSaida]


class ResumoFinanceiroSaida(BaseModel):
    total_receitas: Decimal
    total_despesas: Decimal
    saldo: Decimal

