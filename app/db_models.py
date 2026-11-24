
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
