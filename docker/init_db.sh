#!/bin/bash
set -e

# Чтение значений из переменных окружения
DB_NAME=${DB_NAME:-default_db_name}
DB_USER=${DB_USER:-default_db_user}
DB_PASSWORD=${DB_PASSWORD:-default_db_password}

# Выполнение SQL-команды для создания базы данных, если она не существует
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    DO \$\$
    BEGIN
       IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME') THEN
          CREATE DATABASE "$DB_NAME";
       END IF;
    END
    \$\$;
EOSQL