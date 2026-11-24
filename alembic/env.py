
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool


import os

from sqlalchemy.engine import URL

from app.db_connection import DATABASE_URL
from app.db_models import Base


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Modelos SQLAlchemy que o Alembic deve acompanhar
target_metadata = Base.metadata


# Por padrão, utiliza o banco de desenvolvimento.
database_url = DATABASE_URL

# Permite selecionar explicitamente o banco de testes.
if os.getenv("ALEMBIC_USE_TEST_DB") == "1":
    nome_banco_teste = os.getenv("DB_TEST_NAME")

    if nome_banco_teste != "finance_test_db":
        raise RuntimeError(
            "Banco de testes não configurado corretamente."
        )

    database_url = DATABASE_URL.set(
        database=nome_banco_teste
    )

config.set_main_option(
    "sqlalchemy.url",
    database_url.render_as_string(
        hide_password=False
    ).replace("%", "%%")
)



def run_migrations_offline():
    """Executa migrações sem conexão ativa com o banco."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações conectadas ao PostgreSQL."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
