
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransacaoEntrada(BaseModel):
    descricao: str = Field(min_length=1, max_length=100)
    valor: Decimal = Field(
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2
    )
    tipo: Literal["receita", "despesa"]
