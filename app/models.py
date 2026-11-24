
from decimal import Decimal
from typing import Literal

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


class TransacaoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    valor: Decimal
    tipo: Literal["receita", "despesa"]
    categoria: str | None = None


class ListaTransacoesSaida(BaseModel):
    total: int
    transacoes: list[TransacaoSaida]
