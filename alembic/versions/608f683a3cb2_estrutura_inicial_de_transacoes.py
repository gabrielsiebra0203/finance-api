"""estrutura inicial de transacoes

Revision ID: 608f683a3cb2
Revises:
Create Date: 2026-11-24 13:12:28.173706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '608f683a3cb2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Cria a tabela de transações."""
    op.create_table(
        "transacoes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("descricao", sa.String(length=100), nullable=False),
        sa.Column("valor", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("tipo", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("id", name="transacoes_pkey"),
    )


def downgrade() -> None:
    """Remove a tabela de transações."""
    op.drop_table("transacoes")