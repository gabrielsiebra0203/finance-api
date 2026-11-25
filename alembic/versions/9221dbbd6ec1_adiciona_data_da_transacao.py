"""adiciona data da transacao

Revision ID: 9221dbbd6ec1
Revises: 0fdfd41f4d0f
Create Date: 2026-11-24 19:32:48.787463

"""
from datetime import date
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9221dbbd6ec1'
down_revision: Union[str, Sequence[str], None] = '0fdfd41f4d0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # 1. Cria a coluna permitindo valores nulos
    op.add_column(
        "transacoes",
        sa.Column(
            "data_transacao",
            sa.Date(),
            nullable=True
        )
    )

    # 2. Preenche os registros antigos
    data_referencia = date.today()

    op.execute(
        sa.text(
            "UPDATE transacoes "
            "SET data_transacao = :data_referencia "
            "WHERE data_transacao IS NULL"
        ).bindparams(data_referencia=data_referencia)
    )

    # 3. Torna a coluna obrigatória
    op.alter_column(
        "transacoes",
        "data_transacao",
        existing_type=sa.Date(),
        nullable=False
    )


def downgrade() -> None:
    op.drop_column(
        "transacoes",
        "data_transacao"
    )

