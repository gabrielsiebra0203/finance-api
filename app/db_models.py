
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

from sqlalchemy import Date, Numeric, String

class Base(DeclarativeBase):
    pass


class Transacao(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    descricao: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    categoria: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    data_transacao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today
    )
