#!/bin/bash
set -e

# Чтение значений из переменных окружения
DB_NAME=${DB_NAME:-default_db_name}
DB_USER=${DB_USER:-default_db_user}
DB_PASSWORD=${DB_PASSWORD:-default_db_password}

# Чтение значений из переменных окружения для базы данных для тестов
DB_NAME_TEST=${DB_NAME_TEST:-default_db_name}
DB_USER_TEST=${DB_USER_TEST:-default_db_user}
DB_PASSWORD_TEST=${DB_PASSWORD_TEST:-default_db_password}

# Ensure POSTGRES_USER is set
if [ -z "$POSTGRES_USER" ]; then
  echo "Environment variable POSTGRES_USER is not set."
  exit 1
fi

# Function to create a database if it doesn't exist
create_database() {
  local db_name=$1
  echo "Checking if database $db_name exists"
  if psql -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$db_name'" | grep -q 1; then
    echo "Database $db_name already exists."
  else
    echo "Creating database $db_name"
    psql -U "$POSTGRES_USER" -c "CREATE DATABASE \"$db_name\""
  fi
}

# Create the default database
create_database "$DB_NAME"

# Create the test database
create_database "$DB_NAME_TEST"
