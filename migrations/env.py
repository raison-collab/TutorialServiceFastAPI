import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from config import DB_HOST, DB_PORT, DB_PASSWORD, DB_USER, DB_NAME, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST, \
    DB_USER_TEST, DB_PASSWORD_TEST
from src.auth.database import Base as AuthBase
from src.main_service.models import Base as MainServiceBase

sys.path.append(os.path.join(sys.path[0], 'src'))

config = context.config

# Set database configuration from command line argument or default to main db
db_type = context.get_x_argument(as_dictionary=True).get('db', 'default')

if db_type == 'test':
    config.set_main_option('sqlalchemy.url',
                           f'postgresql://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}')
else:
    config.set_main_option('sqlalchemy.url', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = [AuthBase.metadata, MainServiceBase.metadata]


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
